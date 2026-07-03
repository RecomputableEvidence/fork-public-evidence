/* AHI Viewer v0.2 — Comparison Mode
 * Static, repo-local, read-only.
 * Does not approve, certify, score, authorize, determine compliance,
 * determine admissibility, establish legal sufficiency, decide acceptance,
 * or judge correctness.
 */

const SCENARIO_BUNDLE_URL = "../ahi-viewer-v0_1/data/scenarios_bundle.json";
const COMPARISON_URL = "./data/comparison_pairs.json";

const NON_AUTHORITY_TEXT =
  "Does not approve, certify, score, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, or judge correctness.";

function byId(id) {
  return document.getElementById(id);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function list(items) {
  const safeItems = Array.isArray(items) ? items : [];
  if (safeItems.length === 0) {
    return "<p class=\"muted\">None recorded.</p>";
  }
  return `<ul>${safeItems.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
}

function badges(items) {
  const safeItems = Array.isArray(items) ? items : [];
  if (safeItems.length === 0) {
    return "<span class=\"badge\">None recorded</span>";
  }
  return safeItems.map((item) => `<span class="badge">${escapeHtml(item)}</span>`).join("");
}

function scenarioNumber(scenario) {
  return scenario?.scenario_number ?? scenario?.number ?? "";
}

function scenarioTitle(scenario) {
  return scenario?.title ?? scenario?.scenario_title ?? scenario?.name ?? scenario?.scenario_id ?? "Unknown scenario";
}

function scenarioPath(scenario) {
  return scenario?.scenario_path ?? scenario?.path ?? scenario?.narrative_path ?? scenario?.file_path ?? scenario?.file ?? "";
}

function artifactFiles(scenario) {
  return Array.isArray(scenario?.artifact_files) ? scenario.artifact_files : [];
}

function checkerCoverage(scenario) {
  const coverage = scenario?.checker_coverage;
  if (!coverage || typeof coverage !== "object") {
    return [];
  }
  return Object.entries(coverage)
    .filter(([, value]) => Boolean(value))
    .map(([key]) => key);
}

function selectedFields(scenario) {
  const fields = scenario?.selected_fields;
  if (!fields || typeof fields !== "object") {
    return {};
  }
  return fields;
}

function renderScenario(scenario) {
  const fields = selectedFields(scenario);
  const coverage = checkerCoverage(scenario);

  return `
    <dl>
      <dt>Scenario ID</dt>
      <dd class="code">${escapeHtml(scenario?.scenario_id)}</dd>

      <dt>Number</dt>
      <dd>${escapeHtml(scenarioNumber(scenario))}</dd>

      <dt>Posture</dt>
      <dd>${escapeHtml(scenario?.verification_posture ?? "not recorded")}</dd>

      <dt>Path</dt>
      <dd class="code">${escapeHtml(scenarioPath(scenario))}</dd>

      <dt>Artifact files</dt>
      <dd>${badges(artifactFiles(scenario))}</dd>

      <dt>Checker coverage</dt>
      <dd>${badges(coverage)}</dd>

      <dt>Selected fields</dt>
      <dd>${badges(Object.keys(fields))}</dd>
    </dl>
  `;
}

function renderSummary(pair, left, right) {
  byId("summary").innerHTML = `
    <div class="summary-card">
      <div class="label">Pair</div>
      <div class="value">${escapeHtml(pair.pair_id)}</div>
    </div>
    <div class="summary-card">
      <div class="label">Left</div>
      <div class="value">${escapeHtml(left?.scenario_id)}</div>
    </div>
    <div class="summary-card">
      <div class="label">Right</div>
      <div class="value">${escapeHtml(right?.scenario_id)}</div>
    </div>
    <div class="summary-card">
      <div class="label">Comparison posture</div>
      <div class="value">${escapeHtml(pair.comparison_posture)}</div>
    </div>
  `;
}

function renderBoundaryComparison(pair) {
  const rows = [
    ["Comparison purpose", pair.purpose],
    ["Boundary movement", pair.boundary_movement],
    ["Attempted inference", pair.attempted_inference],
    ["Required revalidation", pair.required_revalidation],
  ];

  byId("boundaryComparison").innerHTML = `
    <table class="diff-table">
      <thead>
        <tr>
          <th>Dimension</th>
          <th>Recorded comparison</th>
        </tr>
      </thead>
      <tbody>
        ${rows.map(([label, value]) => `
          <tr>
            <td>${escapeHtml(label)}</td>
            <td>${Array.isArray(value) ? list(value) : escapeHtml(value ?? "not recorded")}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;
}

function renderSupportedComparison(pair) {
  byId("supportedComparison").innerHTML = `
    <h3>Fork can show</h3>
    ${list(pair.fork_can_show)}
    <h3>Reviewer use</h3>
    ${list(pair.reviewer_use)}
  `;
}

function renderNonClaimsComparison(pair) {
  byId("nonClaimsComparison").innerHTML = `
    <p>${escapeHtml(NON_AUTHORITY_TEXT)}</p>
    ${list(pair.fork_does_not_show)}
  `;
}

function renderCoverageComparison(left, right) {
  const leftArtifacts = artifactFiles(left);
  const rightArtifacts = artifactFiles(right);
  const leftCoverage = checkerCoverage(left);
  const rightCoverage = checkerCoverage(right);

  byId("coverageComparison").innerHTML = `
    <table class="diff-table">
      <thead>
        <tr>
          <th>Dimension</th>
          <th>${escapeHtml(left?.scenario_id)}</th>
          <th>${escapeHtml(right?.scenario_id)}</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Verification posture</td>
          <td>${escapeHtml(left?.verification_posture ?? "not recorded")}</td>
          <td>${escapeHtml(right?.verification_posture ?? "not recorded")}</td>
        </tr>
        <tr>
          <td>Artifact count</td>
          <td>${leftArtifacts.length}</td>
          <td>${rightArtifacts.length}</td>
        </tr>
        <tr>
          <td>Checker coverage</td>
          <td>${badges(leftCoverage)}</td>
          <td>${badges(rightCoverage)}</td>
        </tr>
        <tr>
          <td>Scenario path</td>
          <td class="code">${escapeHtml(scenarioPath(left))}</td>
          <td class="code">${escapeHtml(scenarioPath(right))}</td>
        </tr>
      </tbody>
    </table>
  `;
}

function renderPair(pair, scenarioMap) {
  const left = scenarioMap.get(pair.left_scenario_id);
  const right = scenarioMap.get(pair.right_scenario_id);

  if (!left || !right) {
    byId("summary").innerHTML = `<div class="error">Comparison pair references missing scenario IDs.</div>`;
    return;
  }

  byId("leftTitle").textContent = `${scenarioNumber(left)} — ${scenarioTitle(left)}`;
  byId("rightTitle").textContent = `${scenarioNumber(right)} — ${scenarioTitle(right)}`;
  byId("leftScenario").innerHTML = renderScenario(left);
  byId("rightScenario").innerHTML = renderScenario(right);

  renderSummary(pair, left, right);
  renderBoundaryComparison(pair);
  renderSupportedComparison(pair);
  renderNonClaimsComparison(pair);
  renderCoverageComparison(left, right);
}

async function loadJson(url) {
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed to load ${url}: ${response.status}`);
  }
  return response.json();
}

async function main() {
  const [bundle, comparisons] = await Promise.all([
    loadJson(SCENARIO_BUNDLE_URL),
    loadJson(COMPARISON_URL),
  ]);

  const scenarios = Array.isArray(bundle.scenarios) ? bundle.scenarios : [];
  const pairs = Array.isArray(comparisons.comparison_pairs) ? comparisons.comparison_pairs : [];
  const scenarioMap = new Map(scenarios.map((scenario) => [scenario.scenario_id, scenario]));

  const select = byId("pairSelect");
  select.innerHTML = pairs.map((pair, index) => `
    <option value="${index}">${escapeHtml(pair.label)}</option>
  `).join("");

  select.addEventListener("change", () => {
    renderPair(pairs[Number(select.value)], scenarioMap);
  });

  if (pairs.length > 0) {
    renderPair(pairs[0], scenarioMap);
  } else {
    byId("summary").innerHTML = `<div class="error">No comparison pairs recorded.</div>`;
  }
}

main().catch((error) => {
  byId("summary").innerHTML = `<div class="error">${escapeHtml(error.message)}</div>`;
});
