/**
 * Social Media Privacy Risk Assessment Framework
 * Client API Client
 */

const API_BASE = "/api";

const API = {
  // Questions catalog
  async getQuestions() {
    const res = await fetch(`${API_BASE}/questions`);
    return await res.json();
  },

  // Submit assessment
  async submitAssessment(answers, platform = "Cross-Platform") {
    const res = await fetch(`${API_BASE}/assessment`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers, platform })
    });
    return await res.json();
  },

  // Get assessment by ID
  async getAssessment(id) {
    const res = await fetch(`${API_BASE}/assessment/${id}`);
    return await res.json();
  },

  // Run improvement simulation
  async simulateImprovement(answers, selected_actions) {
    const res = await fetch(`${API_BASE}/assessment/simulate-improvement`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers, selected_actions })
    });
    return await res.json();
  },

  // Get available simulation actions
  async getAvailableImprovements() {
    const res = await fetch(`${API_BASE}/assessment/available-improvements`);
    return await res.json();
  },

  // Get dashboard statistics
  async getDashboardStats() {
    const res = await fetch(`${API_BASE}/dashboard/stats`);
    return await res.json();
  },

  // Analyze JSON profile + posts
  async analyzeJsonPayload(profile, posts) {
    const res = await fetch(`${API_BASE}/analyze-json`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ profile, posts })
    });
    return await res.json();
  },

  // Get privacy checklist
  async getPrivacyChecklist() {
    const res = await fetch(`${API_BASE}/privacy-checklist`);
    return await res.json();
  },

  // Delete assessment (GDPR Right to Erasure)
  async deleteAssessment(id) {
    const res = await fetch(`${API_BASE}/assessment/${id}`, {
      method: "DELETE"
    });
    return await res.json();
  },

  // Extract EXIF Metadata in-memory
  async extractMetadata(imageFile) {
    const formData = new FormData();
    formData.append("image", imageFile);
    const res = await fetch(`${API_BASE}/metadata/extract`, {
      method: "POST",
      body: formData
    });
    return await res.json();
  },

  // Strip EXIF Metadata from image
  async stripMetadata(imageFile) {
    const formData = new FormData();
    formData.append("image", imageFile);
    const res = await fetch(`${API_BASE}/metadata/strip`, {
      method: "POST",
      body: formData
    });
    return await res.blob();
  }
};
