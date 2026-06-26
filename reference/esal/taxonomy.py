# reference/esal/taxonomy.py

from .errors import ESALViolation, StructuralError, GovernanceError, DeterminismError
from .models import State


def classify_success(state: State) -> str:
    """
    Classification for successful replay with no raised ESALViolation.
    For now:
      - If state.validity is True and no violations: return "PASS"
      - If state.validity is False or violations exist: return "G"
        (governance violation was correctly detected)
    """
    if state.validity and not state.violations:
        return "PASS"
    else:
        return "G"


def classify_exception(exc: Exception) -> str:
    """
    Map raised exceptions to S/G/D.
    A-class is reserved for the test harness layer and is not produced here.
    """
    if isinstance(exc, StructuralError):
        return "S"
    if isinstance(exc, GovernanceError):
        return "G"
    if isinstance(exc, DeterminismError):
        return "D"
    if isinstance(exc, ESALViolation) and getattr(exc, "classification", None):
        return exc.classification  # fallback to whatever is set on the exception

    # Unknown error type: treat as structural for now
    return "S"


def classify(state: State | None, exc: Exception | None) -> str:
    """
    High-level helper for runner.py:
      - If exc is not None -> classify_exception(exc)
      - Else -> classify_success(state)
    """
    if exc is not None:
        return classify_exception(exc)
    if state is None:
        # No state and no explicit exception: structural problem.
        return "S"
    return classify_success(state)