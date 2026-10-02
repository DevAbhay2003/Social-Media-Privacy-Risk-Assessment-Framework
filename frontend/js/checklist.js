/**
 * Social Media Privacy Risk Assessment Framework
 * Checklist Controller & Completion Tracker
 */

document.addEventListener("DOMContentLoaded", async () => {
  await loadChecklist();
});

async function loadChecklist() {
  const container = document.getElementById("checklist-items-container");
  container.innerHTML = "";

  try {
    const res = await API.getPrivacyChecklist();
    if (res.status !== "success") return;

    // Group items by category
    const grouped = {};
    res.checklist.forEach(item => {
      if (!grouped[item.category]) grouped[item.category] = [];
      grouped[item.category].push(item);
    });

    Object.entries(grouped).forEach(([catName, items]) => {
      const card = document.createElement("div");
      card.className = "card";
      card.style.marginBottom = "1.5rem";

      const itemsHtml = items.map((item, idx) => `
        <label class="checklist-item" style="cursor: pointer;">
          <input type="checkbox" class="checklist-checkbox" onchange="updateChecklistProgress()">
          <div style="flex: 1;">
            <div style="color: var(--text-main); font-size: 0.95rem;">${item.item}</div>
            <div style="font-size: 0.78rem; color: var(--text-muted);">Priority: <strong style="color: ${item.tier === 'Critical' ? 'var(--risk-critical)' : 'var(--accent-cyan)'};">${item.tier}</strong></div>
          </div>
        </label>
      `).join("");

      card.innerHTML = `
        <h3 class="card-title" style="margin-bottom: 1rem; color: var(--accent-cyan);">📁 ${catName}</h3>
        <div>${itemsHtml}</div>
      `;

      container.appendChild(card);
    });

    updateChecklistProgress();

  } catch (err) {
    console.error("Checklist loading error:", err);
  }
}

window.updateChecklistProgress = function() {
  const checkboxes = document.querySelectorAll(".checklist-checkbox");
  if (checkboxes.length === 0) return;

  const total = checkboxes.length;
  const checked = Array.from(checkboxes).filter(c => c.checked).length;
  const percent = Math.round((checked / total) * 100);

  document.getElementById("checklist-progress-text").textContent = `${checked} of ${total} (${percent}%) Completed`;
  document.getElementById("checklist-progress-bar").style.width = `${percent}%`;
};
