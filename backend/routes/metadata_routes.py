"""
Social Media Privacy Risk Assessment Framework
Safe In-Memory Metadata Extraction & Scrubbing Routes
===================================================
Complies with Privacy by Design:
- Reads EXIF tags entirely in memory without writing the file to disk.
- Never uploads user images to external endpoints.
- Provides EXIF stripping so users can sanitize photos before sharing.
"""

from flask import Blueprint, request, jsonify, send_file
import io
from backend.services.metadata_engine import parse_exif_from_bytes, strip_exif_metadata

metadata_bp = Blueprint("metadata", __name__, url_prefix="/api/metadata")

@metadata_bp.route("/extract", methods=["POST"])
def extract_metadata():
    """
    Parses EXIF metadata in-memory from an uploaded image file.
    Does NOT save the image to disk.
    """
    if "image" not in request.files:
        return jsonify({"status": "error", "message": "No image file provided in 'image' field."}), 400

    file_obj = request.files["image"]
    image_bytes = file_obj.read()

    if len(image_bytes) == 0:
        return jsonify({"status": "error", "message": "Uploaded file is empty."}), 400

    if len(image_bytes) > 20 * 1024 * 1024:
        return jsonify({"status": "error", "message": "File exceeds maximum size of 20MB."}), 413

    metadata = parse_exif_from_bytes(image_bytes)
    return jsonify({
        "status": "success",
        "filename": file_obj.filename,
        "size_bytes": len(image_bytes),
        "metadata": metadata,
        "disclaimer": "Processed 100% in-memory locally. No raw images or location coordinates are stored on disk."
    }), 200

@metadata_bp.route("/strip", methods=["POST"])
def strip_metadata_route():
    """
    Strips all EXIF/APP1 segments from uploaded JPEG and returns the sanitized image stream.
    """
    if "image" not in request.files:
        return jsonify({"status": "error", "message": "No image file provided."}), 400

    file_obj = request.files["image"]
    image_bytes = file_obj.read()
    cleaned_bytes = strip_exif_metadata(image_bytes)

    return send_file(
        io.BytesIO(cleaned_bytes),
        mimetype="image/jpeg",
        as_attachment=True,
        download_name=f"sanitized_{file_obj.filename}"
    )
