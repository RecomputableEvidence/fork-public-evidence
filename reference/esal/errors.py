class ESALViolation(Exception):
    classification: str | None = None


class StructuralError(ESALViolation):
    classification = "S"


class GovernanceError(ESALViolation):
    classification = "G"


class DeterminismError(ESALViolation):
    classification = "D"
