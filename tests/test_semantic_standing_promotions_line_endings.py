import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = ROOT / "tests" / "test_semantic_standing_promotions.py"
SPEC = importlib.util.spec_from_file_location("_semantic_standing_test_helpers", HELPER_PATH)
assert SPEC is not None and SPEC.loader is not None
HELPERS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPERS)

make_surface = HELPERS.make_surface
mutate_json = HELPERS.mutate_json
run_checker = HELPERS.run_checker
sha = HELPERS.sha


def test_23_crlf_source_matches_lf_exact_text_on_all_platforms(tmp_path):
    text = "G01-G09 passed; v0.1.5 is now qualified.\n"
    surface = make_surface(tmp_path, text)
    source, _, _, _, assertions = surface

    source.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
    mutate_json(
        assertions,
        lambda value: value.__setitem__("source_sha256", sha(source.read_bytes())),
    )

    proc, result = run_checker(surface)

    assert proc.returncode == 0
    assert result["overall_action"] == "PASS"
    assert result["findings"][0]["disposition"] == "SUPPORTED_WITHIN_DECLARED_TRANSITION"


def test_24_lf_source_matches_crlf_exact_text_on_all_platforms(tmp_path):
    text = "G01-G09 passed; v0.1.5 is now qualified.\n"
    surface = make_surface(tmp_path, text)
    source, _, _, _, assertions = surface

    source.write_bytes(text.encode("utf-8"))

    def mutate(value):
        value["source_sha256"] = sha(source.read_bytes())
        value["assertions"][0]["exact_text"] = text.replace("\n", "\r\n")

    mutate_json(assertions, mutate)
    proc, result = run_checker(surface)

    assert proc.returncode == 0
    assert result["overall_action"] == "PASS"
    assert result["findings"][0]["disposition"] == "SUPPORTED_WITHIN_DECLARED_TRANSITION"


def test_25_lone_cr_is_not_silently_normalized(tmp_path):
    surface = make_surface(tmp_path, "a\nb")
    source, _, _, _, assertions = surface

    source.write_bytes(b"a\rb")
    mutate_json(
        assertions,
        lambda value: value.__setitem__("source_sha256", sha(source.read_bytes())),
    )

    proc, result = run_checker(surface)

    assert proc.returncode == 3
    assert result["overall_action"] == "INDETERMINATE"
    assert result["findings"][0]["disposition"] == "INDETERMINATE_NORMALIZATION_COVERAGE"
