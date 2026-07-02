/* AHI Viewer v0.1 — static, repo-local, read-only */
const state = {
  bundle: null,
  scenarios: [],
  selectedScenarioId: null,
  postureFilter: "ALL",
  categoryFilter: "ALL",
  activeArtifactIndex: 0
};

const postureGuidance = {
  BASELINE: "Reference failure mode or control scenario. Treat as comparison context, not a Fork claim.",
  STRUCTURAL: "Required files and JSON validity may be enforced, but scenario-specific semantic assertions are not currently present.",
  SEMANTICALLY_VERIFIED: "Artifact and classification checks are wired into the checker path. Treat as primary evidentiary scenario within the repository's bounded claims.",
  SCAFFOLD: "Narrative or placeholder exists. Treat as design scaffold, not a complete artifact-backed scenario."
};

const artifactLabels = {
  BDR: "Boundary Delta Record",
  CBC: "Claim Boundary Contract",
  CCE: "Claim Consumption Event",
  SMR: "System Mapping Receipt",
  UIE: "Unsupported Inheritance Event",
  SLE: "Suppressed Limitations Event",
  APC: "Authority Policy Context",
  PRC: "Policy Reference Context",
  NCP: "Non-Claims Panel",
  ONCP: "Original Non-Claims Panel",
  DME: "Downstream Memo Excerpt",
  MD: "Markdown",
  JSON: "JSON"
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function asArray(value) {
  if (!value) return [];
  return Array.isArray(value) ? value : [value];
}

function unique(values) {
  return [...new Set(asArray(values).filter(Boolean).map(String))];
}

function shortScenarioNumber(scenario) {
  return scenario.scenario_number || (scenario.scenario_id || "").match(/SCENARIO_(\d+)/)?.[1] || "";
}

function postureClass(posture) {
  return `posture posture-${String(posture || "unknown").toLowerCase().replaceAll("_", "-")}`;
}

function renderList(items, emptyText = "No explicit entries in bundle.") {
  const list = unique(items);
  if (!list.length) return `<p class="muted">${escapeHtml(emptyText)}</p>`;
  return `<ul>${list.map(item => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
}

function renderJson(value) {
  return `<pre class="raw">${escapeHtml(JSON.stringify(value, null, 2))}</pre>`;
}

function renderMarkdownText(text) {
  if (!text) return `<p class="muted">No Markdown content loaded.</p>`;
  const lines = String(text).split(/\r?\n/);
  return lines.map(line => {
    if (/^###\s+/.test(line)) return `<h4>${escapeHtml(line.replace(/^###\s+/, ""))}</h4>`;
    if (/^##\s+/.test(line)) return `<h3>${escapeHtml(line.replace(/^##\s+/, ""))}</h3>`;
    if (/^#\s+/.test(line)) return `<h2>${escapeHtml(line.replace(/^#\s+/, ""))}</h2>`;
    if (/^\s*[-*]\s+/.test(line)) return `<p class="md-bullet">• ${escapeHtml(line.replace(/^\s*[-*]\s+/, ""))}</p>`;
    if (/^\s*$/.test(line)) return `<div class="md-gap"></div>`;
    return `<p>${escapeHtml(line)}</p>`;
  }).join("");
}

function getCategories(scenario) {
  const fields = [
    scenario.primary_category,
    ...asArray(scenario.secondary_categories),
    ...asArray(scenario.categories),
    ...asArray(scenario.boundary_effects)
  ];
  const classifications = scenario.selected_fields?.classifications || {};
  if (classifications.claim_consumption_classification?.primary_category) fields.push(classifications.claim_consumption_classification.primary_category);
  if (classifications.unsupported_inheritance_event?.category) fields.push(classifications.unsupported_inheritance_event.category);
  if (classifications.suppressed_limitations_event?.category) fields.push(classifications.suppressed_limitations_event.category);
  return unique(fields);
}

function getFilteredScenarios() {
  return state.scenarios.filter(scenario => {
    const postureOk = state.postureFilter === "ALL" || scenario.verification_posture === state.postureFilter;
    const categories = getCategories(scenario);
    const categoryOk = state.categoryFilter === "ALL" || categories.includes(state.categoryFilter);
    return postureOk && categoryOk;
  });
}

function renderCatalog() {
  const scenarios = getFilteredScenarios();
  const postures = unique(state.scenarios.map(s => s.verification_posture));
  const categories = unique(state.scenarios.flatMap(getCategories)).sort();

  return `
    <section class="panel catalog">
      <div class="section-header">
        <div>
          <p class="eyebrow">Scenario Catalog</p>
          <h2>Simulation Surface</h2>
        </div>
        <div class="filters">
          <label>
            Posture
            <select id="postureFilter">
              <option value="ALL">All</option>
              ${postures.map(p => `<option value="${escapeHtml(p)}" ${state.postureFilter === p ? "selected" : ""}>${escapeHtml(p)}</option>`).join("")}
            </select>
          </label>
          <label>
            Category / effect
            <select id="categoryFilter">
              <option value="ALL">All</option>
              ${categories.map(c => `<option value="${escapeHtml(c)}" ${state.categoryFilter === c ? "selected" : ""}>${escapeHtml(c)}</option>`).join("")}
            </select>
          </label>
        </div>
      </div>

      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Scenario</th>
              <th>Title</th>
              <th>Purpose</th>
              <th>Posture</th>
              <th>Viewer treatment</th>
            </tr>
          </thead>
          <tbody>
            ${scenarios.map(scenario => `
              <tr class="scenario-row ${state.selectedScenarioId === scenario.scenario_id ? "selected" : ""}" data-scenario-id="${escapeHtml(scenario.scenario_id)}">
                <td><strong>${escapeHtml(shortScenarioNumber(scenario))}</strong></td>
                <td>${escapeHtml(scenario.title)}</td>
                <td>${escapeHtml(scenario.purpose || "")}</td>
                <td><span class="${postureClass(scenario.verification_posture)}">${escapeHtml(scenario.verification_posture)}</span></td>
                <td>${escapeHtml(scenario.viewer_treatment?.display_group || scenario.viewer_treatment_label || "")}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    </section>
  `;
}

function renderCheckerCoverage(scenario) {
  const coverage = scenario.checker_coverage || scenario.main_checker || {};
  const rows = [
    ["Included in main checker", coverage.included_in_checker ?? coverage.narrative_file_required],
    ["JSON validated", coverage.json_validated ?? coverage.json_validation],
    ["Scenario-specific semantic assertions", coverage.semantic_assertions_present ?? coverage.semantic_classification_assertions],
    ["Dedicated checker invoked", coverage.dedicated_checker_invoked],
    ["Overclaim scan covered", coverage.overclaim_scan_covered]
  ];

  return `
    <section class="panel">
      <p class="eyebrow">Checker posture</p>
      <h3>Current automated coverage</h3>
      <div class="coverage-grid">
        ${rows.map(([label, value]) => `
          <div class="coverage-card">
            <span>${escapeHtml(label)}</span>
            <strong class="${value ? "yes" : "no"}">${value ? "Yes" : "No"}</strong>
          </div>
        `).join("")}
      </div>
      <p class="note">Scenario 04 and Scenario 05 have scenario-specific semantic checks. Scenario 03 is currently structural only.</p>
    </section>
  `;
}

function renderSupportPanels(scenario) {
  const selected = scenario.selected_fields || {};
  const supports = selected.supports_summary || selected.supported_claims || scenario.supports_summary || [];
  const nonSupports = selected.non_support_summary || selected.non_claims || scenario.non_support_summary || [];
  const unresolved = selected.requires_separate_evidence_summary || selected.unresolved_state || selected.required_revalidation || scenario.requires_separate_evidence_summary || [];

  const scenario05Matrix = scenario.scenario_id === "SCENARIO_05_POLICY_REFERENCE_LAUNDERING_ATTEMPT"
    ? `
      <section class="panel matrix-panel">
        <p class="eyebrow">Scenario 05 reliance matrix</p>
        <h3>Policy reference boundary</h3>
        <div class="matrix">
          ${[
            ["Policy referenced", "supported"],
            ["Policy applied", "not supported"],
            ["Policy satisfied", "not supported"],
            ["Compliance determined", "not supported"],
            ["Onboarding cleared", "not supported"],
            ["Authority transferred", "not supported"]
          ].map(([claim, status]) => `
            <div class="matrix-row">
              <span>${escapeHtml(claim)}</span>
              <strong class="${status === "supported" ? "supported" : "unsupported"}">${escapeHtml(status)}</strong>
            </div>
          `).join("")}
        </div>
      </section>
    `
    : "";

  return `
    <section class="claims-grid">
      <div class="panel">
        <p class="eyebrow">Record supports</p>
        <h3>Claims</h3>
        ${renderList(supports)}
      </div>
      <div class="panel">
        <p class="eyebrow">Record does not support</p>
        <h3>Non-claims / limitations</h3>
        ${renderList(nonSupports)}
      </div>
      <div class="panel">
        <p class="eyebrow">Requires separate evidence</p>
        <h3>Unresolved / revalidation</h3>
        ${renderList(unresolved)}
      </div>
    </section>
    ${scenario05Matrix}
  `;
}

function renderArtifactDrilldown(scenario) {
  const artifacts = asArray(scenario.artifacts).filter(a => a.exists !== false);
  if (!artifacts.length) {
    return `
      <section class="panel">
        <p class="eyebrow">Artifact Drilldown</p>
        <h3>No artifact family loaded</h3>
        <p class="muted">This scenario may be baseline or scaffold-only.</p>
      </section>
    `;
  }

  if (state.activeArtifactIndex >= artifacts.length) state.activeArtifactIndex = 0;
  const active = artifacts[state.activeArtifactIndex];

  const structured = active.parsed
    ? renderJson(active.parsed)
    : renderMarkdownText(active.raw_content || active.raw || "");

  const raw = active.raw_content || active.raw || (active.parsed ? JSON.stringify(active.parsed, null, 2) : "");

  return `
    <section class="panel artifact-panel">
      <div class="section-header">
        <div>
          <p class="eyebrow">Artifact Drilldown</p>
          <h3>${escapeHtml(artifactLabels[active.artifact_type] || active.artifact_type || "Artifact")}</h3>
          <p class="muted">${escapeHtml(active.path || "")}</p>
        </div>
      </div>

      <div class="tabs">
        ${artifacts.map((artifact, index) => `
          <button class="tab ${index === state.activeArtifactIndex ? "active" : ""}" data-artifact-index="${index}">
            ${escapeHtml(artifact.artifact_type || artifact.format || `Artifact ${index + 1}`)}
          </button>
        `).join("")}
      </div>

      <div class="artifact-notice">
        This tab displays record content only. It does not approve, certify, authorize, or judge the underlying workflow.
      </div>

      <details open>
        <summary>Structured view</summary>
        ${structured}
      </details>

      <details>
        <summary>Raw artifact</summary>
        <pre class="raw">${escapeHtml(raw)}</pre>
      </details>
    </section>
  `;
}

function renderScenarioDetail() {
  const scenario = state.scenarios.find(s => s.scenario_id === state.selectedScenarioId) || state.scenarios[0];
  if (!scenario) return `<section class="panel"><h2>No scenarios loaded</h2></section>`;
  state.selectedScenarioId = scenario.scenario_id;

  const categories = getCategories(scenario);
  const guidance = postureGuidance[scenario.verification_posture] || scenario.posture_description || "";

  return `
    <section class="detail">
      <section class="panel hero">
        <div class="section-header">
          <div>
            <p class="eyebrow">Scenario ${escapeHtml(shortScenarioNumber(scenario))}</p>
            <h2>${escapeHtml(scenario.title)}</h2>
            <p>${escapeHtml(scenario.purpose || "")}</p>
          </div>
          <span class="${postureClass(scenario.verification_posture)}">${escapeHtml(scenario.verification_posture)}</span>
        </div>
        <div class="tag-row">
          ${categories.map(c => `<span class="tag">${escapeHtml(c)}</span>`).join("")}
        </div>
        <div class="guidance">
          <strong>Treatment guidance:</strong> ${escapeHtml(guidance)}
        </div>
      </section>

      ${renderCheckerCoverage(scenario)}
      ${renderSupportPanels(scenario)}
      ${renderArtifactDrilldown(scenario)}

      <section class="panel">
        <p class="eyebrow">Scenario narrative</p>
        <details>
          <summary>Show loaded Markdown narrative</summary>
          <div class="markdown">${renderMarkdownText(scenario.narrative_markdown || "")}</div>
        </details>
      </section>
    </section>
  `;
}

function renderApp() {
  const app = document.getElementById("app");
  app.innerHTML = `
    <aside class="sidebar">
      ${renderCatalog()}
    </aside>
    <section class="content">
      ${renderScenarioDetail()}
    </section>
  `;

  document.querySelectorAll(".scenario-row").forEach(row => {
    row.addEventListener("click", () => {
      state.selectedScenarioId = row.dataset.scenarioId;
      state.activeArtifactIndex = 0;
      renderApp();
    });
  });

  document.getElementById("postureFilter")?.addEventListener("change", event => {
    state.postureFilter = event.target.value;
    renderApp();
  });

  document.getElementById("categoryFilter")?.addEventListener("change", event => {
    state.categoryFilter = event.target.value;
    renderApp();
  });

  document.querySelectorAll(".tab").forEach(tab => {
    tab.addEventListener("click", () => {
      state.activeArtifactIndex = Number(tab.dataset.artifactIndex);
      renderApp();
    });
  });
}

async function loadBundle() {
  const app = document.getElementById("app");
  try {
    const response = await fetch("data/scenarios_bundle.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const bundle = await response.json();
    state.bundle = bundle;
    state.scenarios = asArray(bundle.scenarios);
    state.selectedScenarioId = state.scenarios[0]?.scenario_id || null;
    renderApp();
  } catch (error) {
    app.innerHTML = `
      <section class="panel error-panel">
        <h2>Unable to load viewer bundle</h2>
        <p>Expected <code>docs/viewer/ahi-viewer-v0_1/data/scenarios_bundle.json</code>.</p>
        <p>Run this from the repository root:</p>
        <pre class="raw">powershell -ExecutionPolicy Bypass -File scripts\\build_ahi_viewer_data_v0_1.ps1 -ForceOverwrite</pre>
        <p class="muted">${escapeHtml(error.message)}</p>
      </section>
    `;
  }
}

loadBundle();
