"""Adversarial regressions for lost/reverted admissions and false accounting."""
import copy
import importlib.util
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("freshness", ROOT / "scripts/check_standing_freshness_v0_1.py")
freshness = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(freshness)


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE).decode().strip()


@pytest.fixture
def history(tmp_path):
    git(tmp_path, "init")
    git(tmp_path, "config", "user.name", "Test")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    (tmp_path / "docs/experiments").mkdir(parents=True)
    p = tmp_path / "docs/experiments/state.json"
    p.write_text('"original"\n')
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-m", "baseline")
    return tmp_path, git(tmp_path, "rev-parse", "HEAD"), p


def test_detects_admission_even_if_later_reverted(history):
    root, base, p = history
    original = p.read_bytes()
    p.write_text('"changed"\n')
    git(root, "add", ".")
    git(root, "commit", "-m", "admission")
    p.write_bytes(original)
    git(root, "add", ".")
    git(root, "commit", "-m", "revert")
    changes = freshness.recognized_transitions(root, base)
    assert len(changes) == 2
    a, b = list(changes)
    assert a[1:] == tuple(reversed(b[1:]))


def test_detects_uncommitted_addition_and_deletion(history):
    root, base, p = history
    p.unlink()
    (p.parent / "new.json").write_text("{}\n")
    changes = freshness.recognized_transitions(root, base)
    assert any(row[0].endswith("state.json") and row[2] is None for row in changes)
    assert any(row[0].endswith("new.json") and row[1] is None for row in changes)


def test_scope_is_explicit(history):
    root, base, _ = history
    (root / "editorial.md").write_text("Out of scope\n")
    assert freshness.recognized_transitions(root, base) == set()


def test_missing_base_fails(history):
    root, _, _ = history
    with pytest.raises(subprocess.CalledProcessError):
        freshness.recognized_transitions(root, "0" * 40)


def test_recognized_symlink_fails(history):
    root, base, p = history
    (p.parent / "alias.json").symlink_to(p.name)
    with pytest.raises(ValueError, match="symlink"):
        freshness.recognized_transitions(root, base)


def test_current_specimen_and_standing_verify():
    result = freshness.evaluate(ROOT)
    assert result["status"] == "PASS", result["errors"]


def test_missing_accounting_is_not_silently_accepted(monkeypatch):
    monkeypatch.setattr(freshness, "recognized_transitions", lambda *_: {("admissions/new.json", None, "a" * 40)})
    result = freshness.evaluate(ROOT)
    assert any("Unaccounted recognized transition" in e for e in result["errors"])


@pytest.mark.parametrize("change,expected", [
    ("manifest", "manifest binding differs"),
    ("promote", "bounded successor state was promoted"),
    ("route", "does not name the current standing"),
])
def test_binding_and_promotion_failures(monkeypatch, change, expected):
    real_load = freshness.load
    def mutated(path):
        value = copy.deepcopy(real_load(path))
        if path.name == "FORK_CURRENT_WORK_REGISTER_v0_8.json":
            if change == "manifest":
                value["observation"]["manifest_sha256"] = "0" * 64
            if change == "promote":
                value["delta_objects"][1]["receiver_registry_frozen"] = True
        if path.name == "PROGRAM_CHANGE_ACCOUNTING_v0_1.json" and change == "route":
            value["standing_register"] = "old.json"
        return value
    monkeypatch.setattr(freshness, "load", mutated)
    assert any(expected in e for e in freshness.evaluate(ROOT)["errors"])
