class SkillRuntimeError(Exception):
    """Base error for the skill runtime."""


class SkillNotFoundError(SkillRuntimeError):
    """Raised when a skill cannot be resolved."""


class SkillDisabledError(SkillRuntimeError):
    """Raised when a disabled skill is selected for execution."""
