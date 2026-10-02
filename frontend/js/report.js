/**
 * Social Media Privacy Risk Assessment Framework
 * Assessment Report Controller
 */

let currentAssessmentId = null;

document.addEventListener("DOMContentLoaded", async () => {
  const urlParams = new URLSearchParams(window.location.search);
  let id = urlParams.get("id");

  if (!id) {
    // If no ID in URL, fetch most recent assessment from dashboard stats
    try {
      const stats = await API.getDashboardStats();
      if (stats.recent_assessments && stats.recent_assessments.length > 0) {
        id = stats.recent_assessments[0].assessment_id;
      }
    } catch (e) {}
  }

  if (id) {
    await loadAssessmentReport(id);
  } else {
    // Show prompt to run assessment
    document.getElementById("rep-id").textContent = "NO RECORD FOUND";
    alert("No assessment record selected. Please run an assessment first!");
    window.location.href = "/assessment";
  }

  // Delete Record Handler (GDPR Right to Erasure)
  document.getElementById("btn-delete-report").addEventListener("click", async () => {
    if (!currentAssessmentId) return;
    if (confirm(`Are you sure you want to permanently erase assessment '${currentAssessmentId}' from the database? This cannot be undone.`)) {
      const res = await API.deleteAssessment(currentAssessmentId);
      if (res.status === "success") {
        alert("Assessment successfully erased.");
        window.location.href = "/dashboard";
      } else {
        alert("Deletion failed: " + res.message);
      }
    }
  });
});

async function loadAssessmentReport(assessmentId) {
  currentAssessmentId = assessmentId;

  try {
    const res = await API.getAssessment(assessmentId);
    if (res.status !== "success") {
      alert("Failed to load assessment report: " + res.message);
      return;
    }

    const data = res.data;

    // 1. Populate Metadata
    document.getElementById("rep-id").textContent = data.assessment_id;
    document.getElementById("rep-date").textContent = new Date(data.created_at).toLocaleString();
    document.getElementById("rep-platform").textContent = data.platform || "Cross-Platform";

    // 2. Populate Overall Score & Risk Badge
    const scoreElem = document.getElementById("rep-score");
    const badgeElem = document.getElementById("rep-badge");
    const meterFill = document.getElementById("rep-meter-fill");

    scoreElem.textContent = `${data.overall_score}`;
    badgeElem.textContent = `${data.risk_level} RISK`;
    badgeElem.className = `risk-badge risk-${data.risk_level.toLowerCase()}`;

    // Fill bar
    meterFill.style.width = `${Math.min(100, data.overall_score)}%`;
    if (data.overall_score <= 20) {
      meterFill.style.background = "#10b981";
      scoreElem.style.color = "#10b981";
    } else if (data.overall_score <= 40) {
      meterFill.style.background = "#f59e0b";
      scoreElem.style.color = "#f59e0b";
    } else if (data.overall_score <= 70) {
      meterFill.style.background = "#f97316";
      scoreElem.style.color = "#f97316";
    } else {
      meterFill.style.background = "#ef4444";
      scoreElem.style.color = "#ef4444";
    }

    // 3. Render Category Chart & Table
    renderReportCategoryChart(data.category_scores);
    renderCategoryTable(data.category_scores);

    // 4. Render Findings
    renderFindings(data.findings);

    // 5. Render Recommendations
    renderRecommendations(data.recommendations);

    // 6. Render Checklist
    renderChecklist();

  } catch (err) {
    console.error("Report loading error:", err);
  }
}

function renderReportCategoryChart(categoryScores) {
  const ctx = document.getElementById("reportCategoryBarChart").getContext("2d");
  const labels = categoryScores.map(c => c.category_name.split(" ")[0]);
  const data = categoryScores.map(c => c.score);
  const colors = data.map(s => s <= 20 ? "#10b981" : (s <= 40 ? "#f59e0b" : (s <= 70 ? "#f97316" : "#ef4444")));

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Domain Risk (0-100)",
        data: data,
        backgroundColor: colors,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { min: 0, max: 100, ticks: { color: "#9ca3af" }, grid: { color: "#1f2937" } },
        x: { ticks: { color: "#e5e7eb", font: { size: 10 } }, grid: { display: false } }
      },
      plugins: { legend: { display: false } }
    }
  });
}

function renderCategoryTable(categoryScores) {
  const tbody = document.getElementById("rep-cat-table-body");
  tbody.innerHTML = "";

  categoryScores.forEach(c => {
    const tr = document.createElement("tr");
    const rClass = `risk-${(c.risk_level || "low").toLowerCase()}`;
    const weightPercent = Math.round((c.weight || 0.1) * 100);

    tr.innerHTML = `
      <td><code>${c.category_code}</code></td>
      <td><strong>${c.category_name}</strong></td>
      <td><strong>${c.score} / 100</strong></td>
      <td>${weightPercent}%</td>
      <td><span class="risk-badge ${rClass}">${c.risk_level || "MODERATE"}</span></td>
    `;
    tbody.appendChild(tr);
  });
}

function renderFindings(findings) {
  const container = document.getElementById("rep-findings-list");
  container.innerHTML = "";

  if (!findings || findings.length === 0) {
    container.innerHTML = `<div style="padding: 1rem; color: var(--risk-low);">✅ Outstanding hygiene! No significant privacy weaknesses detected.</div>`;
    return;
  }

  findings.forEach(f => {
    const item = document.createElement("div");
    const sevClass = (f.severity || "LOW").toLowerCase();
    item.className = `finding-item ${sevClass}`;

    item.innerHTML = `
      <div style="font-size: 1.3rem;">⚠️</div>
      <div style="flex: 1;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
          <strong style="font-size: 1rem; color: var(--text-main);">${f.title}</strong>
          <span class="risk-badge risk-${sevClass}">${f.severity} SEVERITY</span>
        </div>
        <p style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 0.4rem;">${f.description}</p>
        <div style="font-size: 0.78rem; color: var(--accent-cyan);">
          Domain: ${f.category_name || f.category_code}
        </div>
      </div>
    `;
    container.appendChild(item);
  });
}

function renderRecommendations(recommendations) {
  const container = document.getElementById("rep-recommendations-list");
  container.innerHTML = "";

  if (!recommendations || recommendations.length === 0) {
    container.innerHTML = `<div style="padding: 1rem; color: var(--risk-low);">✅ All tested privacy and account controls are in an optimal posture.</div>`;
    return;
  }

  recommendations.forEach(r => {
    const item = document.createElement("div");
    const prioClass = (r.priority || "GOOD PRACTICE").toLowerCase().replace(" ", "-");
    item.className = `rec-item ${prioClass}`;

    item.innerHTML = `
      <div style="font-size: 1.3rem;">🛡️</div>
      <div style="flex: 1;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
          <strong style="font-size: 1rem; color: var(--text-main);">${r.title}</strong>
          <span class="risk-badge ${prioClass === 'immediate' ? 'risk-critical' : (prioClass === 'important' ? 'risk-high' : 'risk-low')}">${r.priority}</span>
        </div>
        <p style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 0.4rem;">${r.action_steps}</p>
        <div style="font-size: 0.78rem; color: var(--text-dark);">
          Impact: <span style="color: #6ee7b7;">${r.impact_estimate || "Substantial attack surface reduction"}</span>
        </div>
      </div>
    `;
    container.appendChild(item);
  });
}

async function renderChecklist() {
  const container = document.getElementById("rep-checklist-container");
  container.innerHTML = "";

  try {
    const res = await API.getPrivacyChecklist();
    if (res.status === "success") {
      res.checklist.slice(0, 8).forEach(item => {
        const div = document.createElement("div");
        div.className = "checklist-item";
        div.innerHTML = `
          <input type="checkbox">
          <div>
            <div style="font-size: 0.92rem; color: var(--text-main);">${item.item}</div>
            <small style="color: var(--text-muted); font-size: 0.78rem;">${item.category} • Tier: ${item.tier}</small>
          </div>
        `;
        container.appendChild(div);
      });
    }
  } catch (e) {}
}
