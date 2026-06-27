class ESALViolation(Exception):
    classification: str | None = None

    def __init__(
        self,
        message: str,
        *,
        error_code: str | None = None,
        offending_event_id: str | None = None,
        path: str | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.offending_event_id = offending_event_id
        self.path = path


class StructuralError(ESALViolation):
    classification = "S"


class GovernanceError(ESALViolation):
    classification = "G"


class DeterminismError(ESALViolation):
    classification = "D"