/**
 * Social Media Privacy Risk Assessment Framework
 * Assessment Controller & Stepper Logic
 */

let allQuestions = [];
let categoryDefs = {};
let categoryKeys = [];
let currentCatIndex = 0;
let userAnswers = {};

document.addEventListener("DOMContentLoaded", async () => {
  setupModeSwitching();
  await loadQuestionnaire();
  setupDemoButtons();
  setupJsonSampleButtons();
});

// Switch between 44-Question Questionnaire and JSON File Ingestion Mode
function setupModeSwitching() {
  const tabQuestions = document.getElementById("tab-mode-questions");
  const tabJson = document.getElementById("tab-mode-json");
  const secQuestions = document.getElementById("section-questionnaire");
  const secJson = document.getElementById("section-json-mode");

  tabQuestions.addEventListener("click", () => {
    tabQuestions.classList.add("active");
    tabJson.classList.remove("active");
    secQuestions.style.display = "block";
    secJson.style.display = "none";
  });

  tabJson.addEventListener("click", () => {
    tabJson.classList.add("active");
    tabQuestions.classList.remove("active");
    secJson.style.display = "block";
    secQuestions.style.display = "none";
  });
}

// Load Questions from Backend API
async function loadQuestionnaire() {
  try {
    const res = await API.getQuestions();
    if (res.status === "success") {
      allQuestions = res.questions;
      categoryDefs = res.categories;
      categoryKeys = Object.keys(categoryDefs);

      renderCategoryTabs();
      showCategory(0);
    }
  } catch (err) {
    document.getElementById("questions-container").innerHTML = `
      <div style="color: var(--risk-critical); padding: 1.5rem; text-align: center;">
        Failed to load questionnaire: ${err.message}. Ensure backend is running.
      </div>`;
  }
}

// Render Category Navigation Tabs
function renderCategoryTabs() {
  const tabsContainer = document.getElementById("category-tabs");
  tabsContainer.innerHTML = "";

  categoryKeys.forEach((catCode, idx) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = `cat-tab ${idx === 0 ? "active" : ""}`;
    btn.textContent = `${catCode.replace("CAT_", "")}. ${categoryDefs[catCode].name}`;
    btn.dataset.index = idx;
    btn.addEventListener("click", () => showCategory(idx));
    tabsContainer.appendChild(btn);
  });
}

// Display Questions for a Specific Category
function showCategory(index) {
  currentCatIndex = index;
  const catCode = categoryKeys[index];
  const catMeta = categoryDefs[catCode];

  // Update tabs active state
  document.querySelectorAll("#category-tabs .cat-tab").forEach((tab, i) => {
    tab.classList.toggle("active", i === index);
  });

  // Update Category Intro
  document.getElementById("current-cat-name").textContent = `${catCode}: ${catMeta.name} (Weight: ${Math.round(catMeta.weight * 100)}%)`;
  document.getElementById("current-cat-desc").textContent = catMeta.description;

  // Filter Questions for this Category
  const catQuestions = allQuestions.filter(q => q.category_code === catCode);
  const container = document.getElementById("questions-container");
  container.innerHTML = "";

  catQuestions.forEach(q => {
    const card = document.createElement("div");
    card.className = "question-card";

    const selectedVal = userAnswers[q.id] || "";

    const optionsHtml = q.options.map(opt => {
      const isChecked = selectedVal === opt.value;
      return `
        <label class="option-label ${isChecked ? 'selected' : ''}">
          <input type="radio" name="${q.id}" value="${opt.value}" ${isChecked ? 'checked' : ''} onchange="handleAnswerChange('${q.id}', '${opt.value}')">
          <span>${opt.label}</span>
        </label>
      `;
    }).join("");

    card.innerHTML = `
      <div class="question-header">
        <div class="question-text">${q.id}. ${q.question}</div>
      </div>
      <div class="question-help">💡 ${q.help_text}</div>
      <div class="options-group">
        ${optionsHtml}
      </div>
    `;
    container.appendChild(card);
  });

  // Update Stepper Navigation Buttons
  const prevBtn = document.getElementById("btn-prev-cat");
  const nextBtn = document.getElementById("btn-next-cat");
  const submitBtn = document.getElementById("btn-submit-assessment");
  const progressText = document.getElementById("progress-indicator");

  prevBtn.style.visibility = index === 0 ? "hidden" : "visible";
  progressText.textContent = `Category ${index + 1} of ${categoryKeys.length}`;

  if (index === categoryKeys.length - 1) {
    nextBtn.style.display = "none";
    submitBtn.style.display = "inline-flex";
  } else {
    nextBtn.style.display = "inline-flex";
    submitBtn.style.display = "none";
  }

  // Scroll smoothly to top of form
  window.scrollTo({ top: 180, behavior: "smooth" });
}

// Stepper Button Listeners
document.getElementById("btn-prev-cat").addEventListener("click", () => {
  if (currentCatIndex > 0) showCategory(currentCatIndex - 1);
});

document.getElementById("btn-next-cat").addEventListener("click", () => {
  if (currentCatIndex < categoryKeys.length - 1) showCategory(currentCatIndex + 1);
});

// Update In-Memory Answers
window.handleAnswerChange = function(questionId, value) {
  userAnswers[questionId] = value;
  // Update visually selected state on option labels
  const group = document.querySelectorAll(`input[name="${questionId}"]`);
  group.forEach(input => {
    input.closest(".option-label").classList.toggle("selected", input.checked);
  });
};

// Form Submission Handler
document.getElementById("assessment-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const answeredCount = Object.keys(userAnswers).length;
  if (answeredCount < 20) {
    alert(`Please complete at least 20 questions across the categories before submitting (currently answered: ${answeredCount}).`);
    return;
  }

  try {
    const res = await API.submitAssessment(userAnswers, "Cross-Platform");
    if (res.status === "success") {
      // Store current answers temporarily in sessionStorage for the simulator
      sessionStorage.setItem("last_answers", JSON.stringify(userAnswers));
      window.location.href = `/report?id=${res.data.assessment_id}`;
    } else {
      alert("Assessment Error: " + res.message);
    }
  } catch (err) {
    alert("Submission failed: " + err.message);
  }
});

// =========================================================================
// Quick Load Demo Personas (High Exposure vs Defensive Safe)
// =========================================================================
function setupDemoButtons() {
  document.getElementById("btn-load-high-risk").addEventListener("click", () => {
    // Fill all questions with highest risk answers
    allQuestions.forEach(q => {
      // Pick option with maximum risk_points
      const highestRiskOpt = [...q.options].sort((a, b) => b.risk_points - a.risk_points)[0];
      userAnswers[q.id] = highestRiskOpt.value;
    });
    alert("⚠️ High Exposure Demo Profile loaded across all 44 questions!");
    showCategory(currentCatIndex);
  });

  document.getElementById("btn-load-safe").addEventListener("click", () => {
    // Fill all questions with safest answers (0 risk points)
    allQuestions.forEach(q => {
      const safestOpt = [...q.options].sort((a, b) => a.risk_points - b.risk_points)[0];
      userAnswers[q.id] = safestOpt.value;
    });
    alert("✅ Defensive Hardened Profile loaded across all 44 questions!");
    showCategory(currentCatIndex);
  });
}

// =========================================================================
// JSON File Ingestion Mode Helpers
// =========================================================================
const SAMPLE_HIGH_PROFILE = {
  "platform": "instagram",
  "username": "alex.oversharer",
  "display_name": "Alex Mercer",
  "bio": "Senior Dev @ FinTech Corp • Runner • Proud dad of 2 • Reach me at alex.mercer.dev@example.com",
  "website": "https://myportfolio.com/alex",
  "email": "alex.mercer.dev@example.com",
  "phone": "+1 415 555 0199",
  "location": "San Francisco, CA",
  "privacy": {
    "account_private": false,
    "show_activity": true,
    "allow_message_requests": true,
    "search_engine_indexing": true
  },
  "links": [
    "https://linktr.ee/alexmercer",
    "https://github.com/alexmercer",
    "https://pastebin.com/u/alexm"
  ]
};

const SAMPLE_HIGH_POSTS = [
  {
    "id": "post_001",
    "text": "Daily 7am run along the Embarcadero before heading to 3rd floor office at FinTech Corp HQ!",
    "created_at": "2026-06-12T07:15:00Z",
    "hashtags": ["#5k", "#morningroutine", "#running"],
    "mentions": ["@fintechcorp"],
    "geo": {"lat": 37.7937, "lon": -122.3965, "name": "The Embarcadero, SF"},
    "media": {
      "type": "image",
      "has_faces": true,
      "is_child_present": false,
      "exif": {"make": "Apple", "model": "iPhone 15 Pro", "created_local": "2026-06-12 07:10:45"}
    }
  },
  {
    "id": "post_002",
    "text": "Picked up my new employee badge and security pass! Loving my desk setup on 4th floor.",
    "created_at": "2026-06-15T10:30:00Z",
    "hashtags": ["#newjob", "#office", "#badge"],
    "mentions": ["@fintechcorp"],
    "geo": null,
    "media": {"type": "image", "has_faces": true, "is_child_present": false, "exif": null}
  },
  {
    "id": "post_003",
    "text": "Super excited for our family vacation to Maui starting next Monday! Leaving the house empty for 2 whole weeks #kids #vacation #travel",
    "created_at": "2026-07-01T18:45:00Z",
    "hashtags": ["#travel", "#vacation", "#family"],
    "mentions": [],
    "geo": {"lat": 37.7749, "lon": -122.4194, "name": "Home, SF"},
    "media": {"type": "image", "has_faces": true, "is_child_present": true, "exif": {"make": "Sony", "model": "A7 IV"}}
  }
];

const SAMPLE_SAFE_PROFILE = {
  "platform": "instagram",
  "username": "morgan_security_mindset",
  "display_name": "Morgan S.",
  "bio": "Tech enthusiast & photography hobbyist. Opinions are my own.",
  "website": "",
  "email": null,
  "phone": null,
  "location": "California, US",
  "privacy": {
    "account_private": true,
    "show_activity": false,
    "allow_message_requests": false,
    "search_engine_indexing": false
  },
  "links": []
};

const SAMPLE_SAFE_POSTS = [
  {
    "id": "post_safe_001",
    "text": "Attended an insightful technical webinar this afternoon. Great discussions on distributed systems!",
    "created_at": "2026-08-10T19:00:00Z",
    "hashtags": ["#tech", "#learning"],
    "mentions": [],
    "geo": null,
    "media": {"type": "none", "has_faces": false, "is_child_present": false, "exif": null}
  }
];

function setupJsonSampleButtons() {
  const profileArea = document.getElementById("json-profile-input");
  const postsArea = document.getElementById("json-posts-input");

  // Default to High Risk sample for demonstration
  profileArea.value = JSON.stringify(SAMPLE_HIGH_PROFILE, null, 2);
  postsArea.value = JSON.stringify(SAMPLE_HIGH_POSTS, null, 2);

  document.getElementById("btn-load-sample-high").addEventListener("click", () => {
    profileArea.value = JSON.stringify(SAMPLE_HIGH_PROFILE, null, 2);
    postsArea.value = JSON.stringify(SAMPLE_HIGH_POSTS, null, 2);
  });

  document.getElementById("btn-load-sample-safe").addEventListener("click", () => {
    profileArea.value = JSON.stringify(SAMPLE_SAFE_PROFILE, null, 2);
    postsArea.value = JSON.stringify(SAMPLE_SAFE_POSTS, null, 2);
  });

  document.getElementById("btn-submit-json").addEventListener("click", async () => {
    try {
      const prof = JSON.parse(profileArea.value);
      const pst = JSON.parse(postsArea.value);
      const res = await API.analyzeJsonPayload(prof, pst);

      if (res.status === "success") {
        window.location.href = `/report?id=${res.data.assessment_id}`;
      } else {
        alert("JSON Analysis Error: " + res.message);
      }
    } catch (err) {
      alert("Invalid JSON format: " + err.message);
    }
  });
}
