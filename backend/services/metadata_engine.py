"""
Social Media Privacy Risk Assessment Framework
Safe In-Memory Photo & EXIF Metadata Analysis Engine
===================================================
Adheres strictly to Privacy by Design & Data Minimization:
- Operates 100% in-memory without storing raw image files on the disk.
- Never sends image bytes or metadata to external servers or third parties.
- Reads only explicitly present EXIF tags; never infers or guesses hidden data.
- Generates a sanitized copy with all EXIF markers stripped.
"""

import io
import struct
from typing import Dict, Any, Optional

def _convert_dms_to_dd(degrees: float, minutes: float, seconds: float, direction: str) -> float:
    """Converts Degrees Minutes Seconds (DMS) to Decimal Degrees (DD)."""
    dd = float(degrees) + float(minutes)/60.0 + float(seconds)/(3600.0)
    if direction.upper() in ["S", "W"]:
        dd = -dd
    return round(dd, 6)

def parse_exif_from_bytes(image_bytes: bytes) -> Dict[str, Any]:
    """
    Parses EXIF metadata tags safely from image bytes in-memory.
    Inspects standard JPEG App1 and TIFF headers.
    """
    metadata: Dict[str, Any] = {
        "has_exif": False,
        "device_make": None,
        "device_model": None,
        "software": None,
        "date_time_original": None,
        "gps_latitude": None,
        "gps_longitude": None,
        "gps_raw": None,
        "privacy_risks_detected": [],
        "risk_rating": "LOW",
        "raw_tag_count": 0
    }

    if len(image_bytes) < 4:
        return metadata

    # Check JPEG SOI marker (0xFFD8)
    if image_bytes[:2] != b'\xff\xd8':
        # Non-JPEG or raw stream
        return metadata

    # Scan JPEG segments for APP1 (0xFFE1) EXIF marker
    offset = 2
    length = len(image_bytes)

    while offset < length - 4:
        marker = image_bytes[offset:offset+2]
        if marker[0] != 0xff:
            break
        if marker == b'\xff\xda': # Start of Scan (image data)
            break

        seg_len = struct.unpack('>H', image_bytes[offset+2:offset+4])[0]
        seg_data = image_bytes[offset+4:offset+2+seg_len]

        if marker == b'\xff\xe1' and seg_data.startswith(b'Exif\x00\x00'):
            # Found EXIF payload
            metadata["has_exif"] = True
            _parse_tiff_header(seg_data[6:], metadata)
            break

        offset += 2 + seg_len

    # Evaluate privacy risks based on discovered tags
    risks = []
    if metadata.get("gps_latitude") is not None or metadata.get("gps_raw") is not None:
        risks.append({
            "severity": "CRITICAL",
            "type": "GEOLOCATION_LEAK",
            "description": "Image embeds exact GPS coordinates, revealing physical location where photo was captured."
        })
        metadata["risk_rating"] = "CRITICAL"
    if metadata.get("date_time_original"):
        risks.append({
            "severity": "MEDIUM",
            "type": "TIMESTAMP_LEAK",
            "description": f"Creation timestamp ({metadata['date_time_original']}) exposes timeline context."
        })
        if metadata["risk_rating"] != "CRITICAL":
            metadata["risk_rating"] = "MEDIUM"
    if metadata.get("device_model"):
        risks.append({
            "severity": "LOW",
            "type": "HARDWARE_LEAK",
            "description": f"Camera hardware model ({metadata['device_model']}) exposes device signature."
        })

    metadata["privacy_risks_detected"] = risks
    return metadata

def _parse_tiff_header(tiff_bytes: bytes, metadata: Dict[str, Any]):
    """Basic TIFF header parser for Make, Model, DateTime, and GPS tags."""
    if len(tiff_bytes) < 8:
        return

    endian = tiff_bytes[:2]
    fmt_endian = '<' if endian == b'II' else '>'
    
    try:
        magic = struct.unpack(fmt_endian + 'H', tiff_bytes[2:4])[0]
        if magic != 42:
            return
        
        ifd_offset = struct.unpack(fmt_endian + 'I', tiff_bytes[4:8])[0]
        if ifd_offset + 2 > len(tiff_bytes):
            return

        num_entries = struct.unpack(fmt_endian + 'H', tiff_bytes[ifd_offset:ifd_offset+2])[0]
        cur = ifd_offset + 2
        metadata["raw_tag_count"] = num_entries

        # Well-known EXIF Tag IDs:
        # 0x010F: Make, 0x0110: Model, 0x0131: Software, 0x0132: DateTime
        # 0x8825: GPS Info IFD Pointer, 0x9003: DateTimeOriginal
        gps_ifd_offset = None

        for _ in range(min(num_entries, 60)):
            if cur + 12 > len(tiff_bytes):
                break
            tag, dtype, count, val_or_offset = struct.unpack(fmt_endian + 'HHII', tiff_bytes[cur:cur+12])
            cur += 12

            if tag == 0x010F: # Make
                metadata["device_make"] = _read_string(tiff_bytes, val_or_offset, count)
            elif tag == 0x0110: # Model
                metadata["device_model"] = _read_string(tiff_bytes, val_or_offset, count)
            elif tag == 0x0131: # Software
                metadata["software"] = _read_string(tiff_bytes, val_or_offset, count)
            elif tag in (0x0132, 0x9003): # DateTime / DateTimeOriginal
                metadata["date_time_original"] = _read_string(tiff_bytes, val_or_offset, count)
            elif tag == 0x8825: # GPS IFD Pointer
                gps_ifd_offset = val_or_offset

        if gps_ifd_offset and gps_ifd_offset + 2 < len(tiff_bytes):
            metadata["gps_raw"] = "GPS Tag Block Present"
            # Flag GPS coordinates presence
            metadata["gps_latitude"] = "GPS EXIF Data Present"
            metadata["gps_longitude"] = "GPS EXIF Data Present"

    except Exception:
        # Gracefully handle truncated or non-standard headers
        pass

def _read_string(data: bytes, offset: int, length: int) -> Optional[str]:
    """Safely extracts ASCII string from byte offset."""
    try:
        if offset + length <= len(data):
            return data[offset:offset+length].decode("ascii", errors="ignore").strip("\x00 \t\r\n")
    except Exception:
        pass
    return None

def strip_exif_metadata(image_bytes: bytes) -> bytes:
    """
    Produces a sanitized copy of the JPEG image with all APP1/EXIF segments removed.
    Returns: Cleaned image bytes.
    """
    if len(image_bytes) < 4 or image_bytes[:2] != b'\xff\xd8':
        return image_bytes

    out = io.BytesIO()
    out.write(b'\xff\xd8') # SOI

    offset = 2
    length = len(image_bytes)

    while offset < length - 4:
        marker = image_bytes[offset:offset+2]
        if marker[0] != 0xff:
            out.write(image_bytes[offset:])
            break
        if marker == b'\xff\xda': # SOS marker - image scan payload starts
            out.write(image_bytes[offset:])
            break

        seg_len = struct.unpack('>H', image_bytes[offset+2:offset+4])[0]
        
        # Skip APP1 (EXIF / XMP) and APP2 segments
        if marker in (b'\xff\xe1', b'\xff\xe2'):
            offset += 2 + seg_len
            continue

        out.write(image_bytes[offset:offset+2+seg_len])
        offset += 2 + seg_len

    return out.getvalue()
