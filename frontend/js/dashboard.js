/**
 * Social Media Privacy Risk Assessment Framework
 * Dashboard Controller & Chart.js Visualizations
 */

document.addEventListener("DOMContentLoaded", async () => {
  await loadDashboardAnalytics();
});

async function loadDashboardAnalytics() {
  try {
    const res = await API.getDashboardStats();
    if (res.status !== "success") return;

    // 1. Populate Top Stat Boxes
    document.getElementById("stat-total-count").textContent = res.total_assessments_analyzed.toLocaleString();
    document.getElementById("stat-avg-score").textContent = `${res.average_population_risk} / 100`;
    document.getElementById("stat-mfa-rate").textContent = `${res.security_controls_adoption.mfa_adoption}%`;

    const badge = document.getElementById("stat-risk-badge");
    badge.textContent = `${res.risk_level} RISK`;
    badge.className = `risk-badge risk-${res.risk_level.toLowerCase()}`;

    // 2. Render Chart 1: 10-Category Radar Chart
    renderCategoryRadar(res.category_benchmarks);

    // 3. Render Chart 2: Population Risk Tier Distribution (Doughnut)
    renderRiskDistribution(res.risk_distribution);

    // 4. Render Chart 3: Top Systemic Weaknesses (Horizontal Bar)
    renderTopWeaknesses(res.top_weaknesses);

    // 5. Render Chart 4: Security Controls Adoption (Bar Chart)
    renderControlsAdoption(res.security_controls_adoption);

    // 6. Populate Recent Assessments Table
    renderRecentAssessments(res.recent_assessments);

  } catch (err) {
    console.error("Dashboard analytics loading failed:", err);
  }
}

// 1. Radar Chart: 10 Categories
function renderCategoryRadar(benchmarks) {
  const ctx = document.getElementById("categoryRadarChart").getContext("2d");
  const labels = benchmarks.map(b => b.category);
  const data = benchmarks.map(b => b.avg_risk);

  new Chart(ctx, {
    type: "radar",
    data: {
      labels: labels,
      datasets: [{
        label: "Average Risk Score (0-100)",
        data: data,
        backgroundColor: "rgba(99, 102, 241, 0.25)",
        borderColor: "rgba(99, 102, 241, 0.9)",
        pointBackgroundColor: "#06b6d4",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "#06b6d4"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          min: 0,
          max: 100,
          ticks: { stepSize: 20, color: "#9ca3af", backdropColor: "transparent" },
          grid: { color: "#374151" },
          angleLines: { color: "#374151" },
          pointLabels: { color: "#e5e7eb", font: { size: 11, weight: "bold" } }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
}

// 2. Doughnut Chart: Risk Tier Distribution
function renderRiskDistribution(dist) {
  const ctx = document.getElementById("riskDistributionChart").getContext("2d");

  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Low Risk (0-20)", "Moderate Risk (21-40)", "High Risk (41-70)", "Critical Risk (71-100)"],
      datasets: [{
        data: [dist.LOW, dist.MODERATE, dist.HIGH, dist.CRITICAL],
        backgroundColor: ["#10b981", "#f59e0b", "#f97316", "#ef4444"],
        borderColor: "#111827",
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
          labels: { color: "#e5e7eb", boxWidth: 14, font: { size: 11 } }
        }
      }
    }
  });
}

// 3. Horizontal Bar Chart: Top Weaknesses
function renderTopWeaknesses(weaknesses) {
  const ctx = document.getElementById("topWeaknessesChart").getContext("2d");
  const topList = weaknesses.slice(0, 6);

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: topList.map(w => w.weakness),
      datasets: [{
        label: "% Prevalence in Population",
        data: topList.map(w => w.percentage),
        backgroundColor: "rgba(239, 68, 68, 0.7)",
        borderColor: "#ef4444",
        borderWidth: 1,
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          max: 100,
          ticks: { color: "#9ca3af" },
          grid: { color: "#1f2937" }
        },
        y: {
          ticks: { color: "#e5e7eb", font: { size: 11 } },
          grid: { display: false }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
}

// 4. Bar Chart: Security Controls Adoption
function renderControlsAdoption(controls) {
  const ctx = document.getElementById("controlsAdoptionChart").getContext("2d");

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["MFA Active", "Login Alerts", "Tag Review", "Privacy Checkup"],
      datasets: [{
        label: "% Adoption",
        data: [
          controls.mfa_adoption,
          controls.login_alerts_adoption,
          controls.tag_review_adoption,
          controls.privacy_reviews_conducted
        ],
        backgroundColor: [
          "rgba(16, 185, 129, 0.7)",
          "rgba(6, 182, 212, 0.7)",
          "rgba(99, 102, 241, 0.7)",
          "rgba(168, 85, 247, 0.7)"
        ],
        borderWidth: 1,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          max: 100,
          ticks: { color: "#9ca3af" },
          grid: { color: "#1f2937" }
        },
        x: {
          ticks: { color: "#e5e7eb" },
          grid: { display: false }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
}

// 5. Recent Assessments Table
function renderRecentAssessments(assessments) {
  const tbody = document.getElementById("recent-assessments-body");
  tbody.innerHTML = "";

  if (!assessments || assessments.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 1.5rem;">No local assessments recorded yet. Run an assessment to see it listed here!</td></tr>`;
    return;
  }

  assessments.forEach(a => {
    const tr = document.createElement("tr");
    const dateFormatted = new Date(a.created_at).toLocaleString();
    const riskClass = `risk-${a.risk_level.toLowerCase()}`;

    tr.innerHTML = `
      <td><code style="color:var(--accent-cyan);">${a.assessment_id}</code></td>
      <td>${a.platform}</td>
      <td><span style="font-size:0.75rem; background:var(--bg-tertiary); padding:2px 6px; border-radius:4px;">${a.source_type}</span></td>
      <td><strong>${a.overall_score} / 100</strong></td>
      <td><span class="risk-badge ${riskClass}">${a.risk_level}</span></td>
      <td><small style="color:var(--text-muted);">${dateFormatted}</small></td>
      <td><a href="/report?id=${a.assessment_id}" class="btn btn-outline" style="padding: 0.25rem 0.6rem; font-size: 0.75rem;">View Report</a></td>
    `;
    tbody.appendChild(tr);
  });
}
