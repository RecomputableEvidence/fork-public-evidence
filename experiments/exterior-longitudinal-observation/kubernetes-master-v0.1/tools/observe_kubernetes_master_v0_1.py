#!/usr/bin/env python3
"""Read-only GitHub observation for kubernetes/kubernetes:master.

The tool performs at most two unauthenticated GET requests, follows no
redirects, performs no retries, and writes only to the declared local output
directory.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request
from typing import Any

EXPERIMENT_ID = "FORK_ELO_KUBERNETES_MASTER_v0_1"
BRANCH_URL = "https://api.github.com/repos/kubernetes/kubernetes/branches/master"
COMMIT_URL = "https://api.github.com/repos/kubernetes/kubernetes/commits/{sha}"
ALLOWED_HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "fork-exterior-longitudinal-observer-v0.1",
    "X-GitHub-Api-Version": "2022-11-28",
}
PRESERVED_HEADERS = {
    "date", "etag", "last-modified", "x-github-request-id",
    "x-ratelimit-limit", "x-ratelimit-remaining", "x-ratelimit-reset",
    "content-type",
}
NON_CLAIMS = [
    "No claim of Kubernetes internal-state completeness or truth.",
    "No claim of exact underlying transition time or cause.",
    "No claim of safety correctness approval release status or production readiness.",
    "No endorsement or authority transfer from GitHub or Kubernetes.",
]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        raise urllib.error.HTTPError(req.full_url, code, "redirect forbidden", headers, fp)


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso_z(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def reject_credentials() -> None:
    forbidden = [name for name in ("GITHUB_TOKEN", "GH_TOKEN") if os.environ.get(name)]
    if forbidden:
        raise RuntimeError("authenticated credentials forbidden: " + ", ".join(forbidden))


def preserved_headers(headers: Any) -> dict[str, str]:
    return {
        key.lower(): value
        for key, value in headers.items()
        if key.lower() in PRESERVED_HEADERS
    }


def get_once(url: str) -> tuple[int, dict[str, str], bytes]:
    request = urllib.request.Request(url=url, method="GET", headers=ALLOWED_HEADERS)
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=20) as response:
            return response.status, preserved_headers(response.headers), response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read() if exc.fp is not None else b""
        return exc.code, preserved_headers(exc.headers or {}), body


def write_retrieval(root: Path, role: str, url: str, status: int,
                    headers: dict[str, str], body: bytes) -> dict[str, Any]:
    safe = role.lower()
    raw_rel = f"raw/{safe}.bin"
    headers_rel = f"raw/{safe}.headers.json"
    (root / "raw").mkdir(parents=True, exist_ok=True)
    (root / raw_rel).write_bytes(body)
    (root / headers_rel).write_bytes(canonical_bytes(headers))
    return {
        "role": role,
        "url": url,
        "method": "GET",
        "http_status": status,
        "headers": headers,
        "headers_path": headers_rel,
        "raw_path": raw_rel,
        "raw_sha256": sha256_bytes(body),
        "raw_size_bytes": len(body),
    }


def parse_json_object(data: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(data.decode("utf-8"))
    except Exception as exc:
        raise ValueError(f"{label} is not valid UTF-8 JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def derive_projection(branch_body: bytes, commit_body: bytes) -> dict[str, Any]:
    branch = parse_json_object(branch_body, "branch response")
    commit = parse_json_object(commit_body, "commit response")
    branch_commit = branch.get("commit")
    commit_tree = commit.get("commit", {}).get("tree", {})
    parents = commit.get("parents")
    if not isinstance(branch_commit, dict) or not isinstance(branch_commit.get("sha"), str):
        raise ValueError("branch response missing commit.sha")
    if commit.get("sha") != branch_commit["sha"]:
        raise ValueError("commit response SHA does not match branch head SHA")
    if not isinstance(commit_tree.get("sha"), str):
        raise ValueError("commit response missing commit.tree.sha")
    if not isinstance(parents, list) or any(not isinstance(p, dict) or not isinstance(p.get("sha"), str) for p in parents):
        raise ValueError("commit response parents malformed")
    return {
        "branch_name": branch.get("name"),
        "head_sha": branch_commit["sha"],
        "head_tree_sha": commit_tree["sha"],
        "parent_shas": [p["sha"] for p in parents],
        "protected": branch.get("protected"),
    }


def load_previous(path: Path | None) -> dict[str, str] | None:
    if path is None:
        return None
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8"))
    return {
        "observation_id": value["observation_id"],
        "record_sha256": sha256_bytes(raw),
    }


def tool_sha256() -> str:
    return sha256_bytes(Path(__file__).read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--previous-observation", type=Path)
    args = parser.parse_args()

    started = utc_now()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=False)

    findings: list[str] = []
    unresolved = [
        "UNDERLYING_CHANGE_TIME",
        "CAUSE",
        "INTERMEDIATE_STATE_COMPLETENESS",
        "SOURCE_TRUTH_AND_COMPLETENESS",
        "EXTERNAL_AUTHORITY_EFFECT",
    ]
    retrievals: list[dict[str, Any]] = []
    projection = None
    projection_sha = None
    retrieval_status = "RETRIEVAL_FAILED"

    try:
        reject_credentials()
        branch_status, branch_headers, branch_body = get_once(BRANCH_URL)
        retrievals.append(write_retrieval(
            out, "BRANCH_REPRESENTATION", BRANCH_URL,
            branch_status, branch_headers, branch_body
        ))
        if branch_status != 200:
            findings.append("BRANCH_RETRIEVAL_NON_200")
        else:
            branch_obj = parse_json_object(branch_body, "branch response")
            head_sha = branch_obj.get("commit", {}).get("sha")
            if not isinstance(head_sha, str) or len(head_sha) != 40:
                raise ValueError("branch response missing 40-character commit SHA")
            commit_url = COMMIT_URL.format(sha=head_sha)
            commit_status, commit_headers, commit_body = get_once(commit_url)
            retrievals.append(write_retrieval(
                out, "COMMIT_REPRESENTATION", commit_url,
                commit_status, commit_headers, commit_body
            ))
            if commit_status != 200:
                findings.append("COMMIT_RETRIEVAL_NON_200")
            else:
                projection = derive_projection(branch_body, commit_body)
                projection_sha = sha256_bytes(canonical_bytes(projection))
                retrieval_status = "OBSERVED"
    except Exception as exc:
        findings.append(f"OBSERVER_EXCEPTION:{type(exc).__name__}:{exc}")

    completed = utc_now()
    seed = f"{iso_z(started)}|{projection_sha}|{retrievals[0]['raw_sha256'] if retrievals else 'none'}".encode()
    observation_id = started.strftime("K8S-MASTER-OBS-%Y%m%dT%H%M%SZ-") + sha256_bytes(seed)[:12]
    source_date = next(
        (r["headers"].get("date") for r in retrievals if r["headers"].get("date")),
        None,
    )
    record = {
        "schema_version": "0.1",
        "experiment_id": EXPERIMENT_ID,
        "observation_id": observation_id,
        "observer": {
            "tool": "tools/observe_kubernetes_master_v0_1.py",
            "tool_sha256": tool_sha256(),
            "parser_version": "0.1",
            "runtime": sys.version.split()[0],
        },
        "source": {
            "operator": "GitHub",
            "repository": "kubernetes/kubernetes",
            "branch": "master",
            "branch_endpoint": BRANCH_URL,
            "commit_endpoint_template": COMMIT_URL,
        },
        "request_policy": {
            "method": "GET",
            "authenticated": False,
            "automatic_retries": 0,
            "redirects_followed": False,
            "maximum_requests": 2,
        },
        "timing": {
            "started_at_utc": iso_z(started),
            "completed_at_utc": iso_z(completed),
            "source_date_header": source_date,
        },
        "retrieval_status": retrieval_status,
        "retrievals": retrievals,
        "projection": projection,
        "projection_sha256": projection_sha,
        "previous_observation": load_previous(args.previous_observation),
        "findings": findings,
        "unresolved": unresolved,
        "effects": {
            "source_modification": "NONE",
            "fork_repository_mutation": "NONE",
            "authority": "NONE",
            "admission": "NONE",
            "execution": "NONE",
            "truth": "NONE",
            "causality": "NONE",
            "endorsement": "NONE",
        },
        "non_claims": NON_CLAIMS,
    }
    (out / "observation.json").write_bytes(canonical_bytes(record))
    print(retrieval_status)
    print(f"observation_id: {observation_id}")
    print(f"output_dir: {out}")
    return 0 if retrieval_status == "OBSERVED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
