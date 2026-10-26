import json
from pathlib import Path
import shutil
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import prepare_csh_s002_coding_v0_1 as coding


def test_collection_reconciles():
    summary, units, rows = coding.verify()
    assert summary["recorded_file_hashes_verified"] == 94
    assert summary["including_neutral_reported_usd"] == "0.01185"
    assert summary["gross_reserved_usd"] == "0.78"
    assert len(units) == len({r["unit_id"] for r in rows}) == 24
    assert [r["parser_status"] for r in rows] == ["PASS"] * 23 + ["FAIL"]


@pytest.mark.parametrize("mutation", ["bytes", "missing", "extra", "reordered"])
def test_tampered_collection_rejected(tmp_path, mutation):
    collection = tmp_path / "collection"
    shutil.copytree(coding.COLLECTION / "raw", collection / "raw")
    shutil.copyfile(coding.COLLECTION / "PRESERVATION_MANIFEST.json",
                    collection / "PRESERVATION_MANIFEST.json")
    target = collection / "raw" / "ledger.json"
    if mutation == "bytes":
        target.write_bytes(target.read_bytes() + b" ")
    elif mutation == "missing":
        target.unlink()
    elif mutation == "extra":
        (collection / "raw" / "extra.txt").write_text("unexpected")
    else:
        ledger = coding.load(target)
        ledger["results"].reverse()
        coding.save(target, ledger)
        manifest_path = collection / "PRESERVATION_MANIFEST.json"
        manifest = coding.load(manifest_path)
        manifest["files"]["ledger.json"] = coding.prep.digest(target.read_bytes())
        coding.save(manifest_path, manifest)
    with pytest.raises(ValueError):
        coding.verify(collection)


def test_materials_reproduce_and_remain_unscored(tmp_path):
    out = tmp_path / "materials"
    coding.prepare(out)
    expected = coding.COLLECTION / "materials"
    generated = {p.relative_to(out) for p in out.rglob("*") if p.is_file()}
    assert generated == {p.relative_to(expected) for p in expected.rglob("*") if p.is_file()}
    for rel in generated:
        assert (out / rel).read_bytes() == (expected / rel).read_bytes(), str(rel)
    summary = coding.load(out / "analysis/UNSCORED_SUMMARY.json")
    assert summary["run_count"] == 24
    assert summary["classifiable_run_count"] == 0
    assert all(row[k] is None for row in summary["run_rows"] for k in ("U", "P", "A"))
    key = coding.load(out / "coordinator/CODING_KEY.json")
    assert sum(row["primary_grammar_eligible"] for row in key) == 23
    for row in key:
        code = row["coding_id"]
        raw = coding.COLLECTION / "raw" / row["unit_id"] / "output.txt"
        assert (out / "coder-packets" / code / "output.txt").read_bytes() == raw.read_bytes()
        for coder in ("coder-1-templates", "coder-2-templates"):
            template = coding.load(out / coder / (code + ".json"))
            assert template["coder_id"] is None
            assert all(v is None for v in template["normalized_output"].values())
            assert not {"model", "condition", "parser_status"} & template.keys()
    with pytest.raises(FileExistsError):
        coding.prepare(out)


def test_final_examination_preserves_full_text_and_failure():
    _, units, _ = coding.verify()
    raw = (coding.COLLECTION / "raw" / units[-1]["unit_id"] / "output.txt").read_bytes()
    examination = coding.examine_final(raw)
    body = raw[examination["body_utf8_start"]:examination["body_utf8_end"]]
    assert coding.prep.digest(body) == examination["body_sha256"]
    assert json.loads(body) == examination["parsed_object"]
    assert examination["prefix_text"].strip()
    assert examination["primary_eligibility_changed"] is False
    response = coding.load(coding.COLLECTION / "raw" / units[-1]["unit_id"] / "response.bin")
    result, _, parsed = coding.parser.assess_response(response, units[-1]["request"]["model"])
    assert result["errors"] == ["transfer_json_object"]
    assert parsed is None


def test_unicode_examination_offsets():
    raw = 'Préface\n```json\n{"label":"é"}\n```\nSuffix'.encode()
    examination = coding.examine_final(raw)
    assert json.loads(raw[examination["body_utf8_start"]:examination["body_utf8_end"]]) == {"label": "é"}
    assert examination["suffix_text"] == "\nSuffix"


@pytest.mark.parametrize("raw", [b'{}', b'```json\n{}',
    b'```json\n{}\n```\n```json\n{}\n```',
    b'```json\n[]\n```', b'```json\n{"x":1,"x":2}\n```'])
def test_offline_extraction_rejects_ambiguous_or_invalid(raw):
    with pytest.raises(ValueError):
        coding.examine_final(raw)
