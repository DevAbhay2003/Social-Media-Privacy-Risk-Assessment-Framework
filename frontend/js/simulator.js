/**
 * Social Media Privacy Risk Assessment Framework
 * Simulator Controller & Live Recalculation Engine
 */

let availableActions = {};
let selectedActions = new Set([
  "make_phone_private",
  "disable_live_location",
  "enable_mfa",
  "enable_tag_review"
]);
let deltaChart = null;

// Baseline answers default to a typical high-exposure profile
let baseAnswers = {
  "Q_A1": "PUBLIC",
  "Q_A2": "YES",
  "Q_A3": "YES",
  "Q_A4": "YES",
  "Q_B1": "YES",
  "Q_B2": "YES",
  "Q_B3": "YES",
  "Q_B4": "YES",
  "Q_B5": "YES",
  "Q_C1": "YES",
  "Q_C2": "YES",
  "Q_C3": "YES",
  "Q_C4": "YES",
  "Q_C5": "YES",
  "Q_D1": "PUBLIC",
  "Q_D2": "YES",
  "Q_D3": "YES",
  "Q_D4": "YES",
  "Q_E1": "YES",
  "Q_E2": "YES",
  "Q_E3": "YES",
  "Q_E4": "NO",
  "Q_F1": "NO",
  "Q_F2": "YES",
  "Q_F3": "YES",
  "Q_F4": "NO",
  "Q_G1": "NO",
  "Q_G2": "NONE",
  "Q_G3": "YES",
  "Q_G4": "NO",
  "Q_G5": "NO",
  "Q_H1": "YES",
  "Q_H2": "NO",
  "Q_H3": "NO",
  "Q_H4": "YES",
  "Q_I1": "YES",
  "Q_I2": "YES",
  "Q_I3": "YES",
  "Q_I4": "YES",
  "Q_I5": "YES",
  "Q_J1": "NO",
  "Q_J2": "YES",
  "Q_J3": "NO",
  "Q_J4": "NO"
};

document.addEventListener("DOMContentLoaded", async () => {
  // If user completed an assessment recently, use their answers as baseline!
  const stored = sessionStorage.getItem("last_answers");
  if (stored) {
    try {
      baseAnswers = JSON.parse(stored);
    } catch (e) {}
  }

  await loadActionCatalog();
  setupBulkButtons();
  await runSimulation();
});

async function loadActionCatalog() {
  try {
    const res = await API.getAvailableImprovements();
    if (res.status === "success") {
      availableActions = res.actions;
      renderTogglesList();
    }
  } catch (err) {
    console.error("Failed to load actions catalog:", err);
  }
}

function renderTogglesList() {
  const container = document.getElementById("simulator-toggles-list");
  container.innerHTML = "";

  Object.entries(availableActions).forEach(([actionKey, meta]) => {
    const card = document.createElement("div");
    card.className = "simulator-toggle-card";

    const isChecked = selectedActions.has(actionKey);

    card.innerHTML = `
      <div style="padding-right: 1rem;">
        <div style="font-weight: 600; font-size: 0.95rem; color: var(--text-main); margin-bottom: 0.2rem;">
          ${meta.label}
        </div>
        <div style="font-size: 0.78rem; color: var(--text-muted);">
          Domain: <code>${meta.category}</code> • Target: Safe configuration
        </div>
      </div>
      <div>
        <label class="switch">
          <input type="checkbox" data-action="${actionKey}" ${isChecked ? "checked" : ""}>
          <span class="slider"></span>
        </label>
      </div>
    `;

    card.querySelector("input").addEventListener("change", (e) => {
      if (e.target.checked) {
        selectedActions.add(actionKey);
      } else {
        selectedActions.delete(actionKey);
      }
      runSimulation();
    });

    container.appendChild(card);
  });
}

function setupBulkButtons() {
  document.getElementById("btn-select-all").addEventListener("click", () => {
    Object.keys(availableActions).forEach(k => selectedActions.add(k));
    renderTogglesList();
    runSimulation();
  });

  document.getElementById("btn-clear-all").addEventListener("click", () => {
    selectedActions.clear();
    renderTogglesList();
    runSimulation();
  });
}

async function runSimulation() {
  try {
    const res = await API.simulateImprovement(baseAnswers, Array.from(selectedActions));
    if (res.status !== "success") return;

    const data = res.data;

    // Update Scores
    document.getElementById("sim-current-score").textContent = data.original_score;
    const curBadge = document.getElementById("sim-current-badge");
    curBadge.textContent = `${data.original_risk_level} RISK`;
    curBadge.className = `risk-badge risk-${data.original_risk_level.toLowerCase()}`;

    document.getElementById("sim-new-score").textContent = data.simulated_score;
    const newBadge = document.getElementById("sim-new-badge");
    newBadge.textContent = `${data.simulated_risk_level} RISK`;
    newBadge.className = `risk-badge risk-${data.simulated_risk_level.toLowerCase()}`;

    document.getElementById("sim-delta-score").textContent = `-${data.points_reduced}`;
    document.getElementById("sim-delta-percent").textContent = `${data.percent_reduction}% LOWER RISK`;

    // Render / Update Comparison Delta Chart
    renderDeltaChart(data.category_comparison);

  } catch (err) {
    console.error("Simulation failed:", err);
  }
}

function renderDeltaChart(comparison) {
  const ctx = document.getElementById("simulatorDeltaChart").getContext("2d");
  const labels = comparison.map(c => c.category_name);
  const origData = comparison.map(c => c.original_score);
  const simData = comparison.map(c => c.simulated_score);

  if (deltaChart) {
    deltaChart.data.labels = labels;
    deltaChart.data.datasets[0].data = origData;
    deltaChart.data.datasets[1].data = simData;
    deltaChart.update();
    return;
  }

  deltaChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Baseline Risk",
          data: origData,
          backgroundColor: "rgba(239, 68, 68, 0.7)",
          borderColor: "#ef4444",
          borderWidth: 1,
          borderRadius: 3
        },
        {
          label: "Simulated Risk",
          data: simData,
          backgroundColor: "rgba(16, 185, 129, 0.7)",
          borderColor: "#10b981",
          borderWidth: 1,
          borderRadius: 3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          min: 0,
          max: 100,
          ticks: { color: "#9ca3af" },
          grid: { color: "#1f2937" }
        },
        x: {
          ticks: { color: "#e5e7eb", font: { size: 10 } },
          grid: { display: false }
        }
      },
      plugins: {
        legend: {
          labels: { color: "#e5e7eb", boxWidth: 12 }
        }
      }
    }
  });
}
