/**
 * Social Media Privacy Risk Assessment Framework
 * Safe In-Memory Metadata Inspector Controller
 */

let currentImageFile = null;

document.addEventListener("DOMContentLoaded", () => {
  setupDropZone();
  setupDemoButton();
});

function setupDropZone() {
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input");

  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.style.borderColor = "var(--accent-cyan)";
    dropZone.style.background = "rgba(6, 182, 212, 0.08)";
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.style.borderColor = "var(--border-color)";
    dropZone.style.background = "var(--bg-tertiary)";
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.style.borderColor = "var(--border-color)";
    dropZone.style.background = "var(--bg-tertiary)";
    if (e.dataTransfer.files.length > 0) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
      handleFileSelection(e.target.files[0]);
    }
  });

  document.getElementById("btn-strip-download").addEventListener("click", async () => {
    if (!currentImageFile) return;
    try {
      const blob = await API.stripMetadata(currentImageFile);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `sanitized_${currentImageFile.name || "image.jpg"}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("Failed to sanitize image: " + err.message);
    }
  });
}

async function handleFileSelection(file) {
  currentImageFile = file;

  try {
    const res = await API.extractMetadata(file);
    if (res.status === "success") {
      renderMetadataResults(res.filename, res.size_bytes, res.metadata);
    } else {
      alert("Extraction failed: " + res.message);
    }
  } catch (err) {
    alert("Metadata extraction error: " + err.message);
  }
}

function renderMetadataResults(filename, size, meta) {
  const container = document.getElementById("results-container");
  container.style.display = "block";

  document.getElementById("res-filename").textContent = `${filename} (${Math.round(size / 1024)} KB)`;

  const riskBadge = document.getElementById("res-risk-badge");
  const rating = meta.risk_rating || "LOW";
  riskBadge.textContent = `${rating} RISK`;
  riskBadge.className = `risk-badge risk-${rating.toLowerCase()}`;

  // Render Hazards
  const hazardsBox = document.getElementById("res-hazards-box");
  hazardsBox.innerHTML = "";

  if (meta.privacy_risks_detected && meta.privacy_risks_detected.length > 0) {
    meta.privacy_risks_detected.forEach(r => {
      const div = document.createElement("div");
      div.className = `finding-item ${r.severity.toLowerCase()}`;
      div.innerHTML = `
        <div style="font-size: 1.2rem;">⚠️</div>
        <div>
          <strong style="color:var(--text-main); font-size:0.95rem;">${r.type}</strong>
          <div style="font-size:0.85rem; color:var(--text-muted);">${r.description}</div>
        </div>
      `;
      hazardsBox.appendChild(div);
    });
  } else {
    hazardsBox.innerHTML = `<div style="padding:0.75rem; background:rgba(16,185,129,0.1); color:#6ee7b7; border-radius:4px;">✅ No sensitive EXIF tags or GPS coordinates found in this image.</div>`;
  }

  // Render Tags Table
  const tbody = document.getElementById("res-tags-body");
  tbody.innerHTML = "";

  const tagRows = [
    { name: "Camera Manufacturer", val: meta.device_make || "Not Present", risk: meta.device_make ? "Low (Hardware profiling)" : "None" },
    { name: "Camera Model", val: meta.device_model || "Not Present", risk: meta.device_model ? "Low (Device correlation)" : "None" },
    { name: "Software / Firmware", val: meta.software || "Not Present", risk: meta.software ? "Low (OS fingerprinting)" : "None" },
    { name: "Capture Timestamp", val: meta.date_time_original || "Not Present", risk: meta.date_time_original ? "Medium (Timeline exposure)" : "None" },
    { name: "GPS Coordinates", val: meta.gps_latitude || "Not Present", risk: meta.gps_latitude ? "Critical (Physical Geolocation Leak)" : "None" },
    { name: "Total EXIF Tags", val: meta.raw_tag_count || "0", risk: "Information density" }
  ];

  tagRows.forEach(row => {
    const tr = document.createElement("tr");
    const isCritical = row.risk.includes("Critical");
    const isMedium = row.risk.includes("Medium");

    tr.innerHTML = `
      <td><strong>${row.name}</strong></td>
      <td style="font-family: monospace; color: ${isCritical ? 'var(--risk-critical)' : 'var(--text-main)'};">${row.val}</td>
      <td><small style="color: ${isCritical ? 'var(--risk-critical)' : (isMedium ? 'var(--risk-moderate)' : 'var(--text-muted)')}; font-weight: 600;">${row.risk}</small></td>
    `;
    tbody.appendChild(tr);
  });

  // Scroll to results
  container.scrollIntoView({ behavior: "smooth" });
}

// 1-Click Demo Image Generator with synthetic EXIF byte payload
function setupDemoButton() {
  document.getElementById("btn-create-demo-exif").addEventListener("click", () => {
    // Generate a minimal valid JPEG SOI, APP1 EXIF segment with GPS, and EOI
    // JPEG SOI: FF D8
    // APP1 Marker: FF E1
    // Length: 00 5E
    // Exif\0\0
    // TIFF header (Big Endian): 4D 4D 00 2A 00 00 00 08
    const bytes = new Uint8Array([
      0xFF, 0xD8,                                           // SOI
      0xFF, 0xE1, 0x00, 0x36,                               // APP1 Marker + Length (54 bytes)
      0x45, 0x78, 0x69, 0x66, 0x00, 0x00,                   // "Exif\0\0"
      0x4D, 0x4D, 0x00, 0x2A, 0x00, 0x00, 0x00, 0x08,       // TIFF Header (MM, 42, IFD offset 8)
      0x00, 0x02,                                           // 2 IFD tags
      // Tag 1: Make (0x010F), ASCII(2), count 6, offset 32
      0x01, 0x0F, 0x00, 0x02, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x20,
      // Tag 2: GPS IFD Pointer (0x8825), LONG(4), count 1, offset 38
      0x88, 0x25, 0x00, 0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x26,
      0x00, 0x00, 0x00, 0x00,                               // Next IFD offset
      0x41, 0x70, 0x70, 0x6C, 0x65, 0x00,                   // "Apple\0"
      0x00, 0x01,                                           // GPS IFD (1 entry)
      0x00, 0x01, 0x00, 0x02, 0x00, 0x00, 0x00, 0x02, 0x4E, 0x00, 0x00, 0x00, // GPS Latitude Ref 'N'
      0xFF, 0xDA, 0x00, 0x08, 0x01, 0x01, 0x00, 0x00, 0x3F, 0x00, // SOS
      0x00,                                                 // Pixel payload
      0xFF, 0xD9                                            // EOI
    ]);

    const demoFile = new File([bytes], "demo_photo_with_gps.jpg", { type: "image/jpeg" });
    handleFileSelection(demoFile);
  });
}
