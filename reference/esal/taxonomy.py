from .errors import ESALViolation
from .models import State


def classify(state: State | None = None, exc: Exception | None = None) -> str:
    if exc is not None:
        if isinstance(exc, ESALViolation) and exc.classification:
            return exc.classification

        return "S"

    if state is not None and not state.validity:
        return "G"

    return "PASS"


def exception_to_dict(exc: Exception | None) -> dict | None:
    if exc is None:
        return None

    return {
        "type": exc.__class__.__name__,
        "message": str(exc),
        "classification": getattr(exc, "classification", None),
        "error_code": getattr(exc, "error_code", None),
        "offending_event_id": getattr(exc, "offending_event_id", None),
        "path": getattr(exc, "path", None),
    }