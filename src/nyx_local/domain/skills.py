from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

type JsonPrimitive = str | int | float | bool | None
type JsonValue = JsonPrimitive | list[JsonValue] | dict[str, JsonValue]


@dataclass(slots=True, frozen=True)
class SkillParameter:
    """Serializable input parameter announced to Nyx OS."""

    type: str
    required: bool = False
    description: str | None = None

    def to_wire(self) -> dict[str, JsonValue]:
        payload: dict[str, JsonValue] = {
            "type": self.type,
            "required": self.required,
        }
        if self.description is not None:
            payload["description"] = self.description
        return payload


@dataclass(slots=True, frozen=True)
class SkillDescriptor:
    """Public metadata for a locally executable skill."""

    id: str
    name: str
    description: str
    version: str
    parameters: dict[str, SkillParameter] = field(default_factory=dict)
    result_description: str | None = None

    def to_wire(self) -> dict[str, JsonValue]:
        payload: dict[str, JsonValue] = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "parameters": {
                name: parameter.to_wire() for name, parameter in self.parameters.items()
            },
        }
        if self.result_description is not None:
            payload["resultDescription"] = self.result_description
        return payload


@dataclass(slots=True, frozen=True)
class SkillError:
    """Structured execution failure safe to return through the gateway."""

    code: str
    message: str
    retryable: bool = False
    details: dict[str, JsonValue] = field(default_factory=dict)

    def to_wire(self) -> dict[str, JsonValue]:
        payload: dict[str, JsonValue] = {
            "code": self.code,
            "message": self.message,
            "retryable": self.retryable,
        }
        if self.details:
            payload["details"] = self.details
        return payload


@dataclass(slots=True, frozen=True)
class SkillResult:
    """Success or failure returned by every skill execution."""

    success: bool
    result: JsonValue = None
    error: SkillError | None = None

    @classmethod
    def succeeded(cls, result: JsonValue) -> SkillResult:
        return cls(success=True, result=result)

    @classmethod
    def failed(cls, error: SkillError) -> SkillResult:
        return cls(success=False, error=error)


class Skill(ABC):
    """Minimal executable skill contract for the communication foundation."""

    @property
    @abstractmethod
    def descriptor(self) -> SkillDescriptor:
        """Return metadata announced to Nyx OS."""

    @abstractmethod
    def execute(self, input_value: JsonValue) -> SkillResult:
        """Execute with serializable input and return a structured result."""


class SkillRegistry:
    """Registry dedicated to local skills without replacing the core Registry."""

    _ALLOWED_PREFIXES = ("local.", "computer.")

    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        skill_id = skill.descriptor.id
        if not skill_id.startswith(self._ALLOWED_PREFIXES):
            raise ValueError(f"Skill id must start with local. or computer.: {skill_id}")
        if skill_id in self._skills:
            raise ValueError(f"Skill already registered: {skill_id}")
        self._skills[skill_id] = skill

    def get(self, skill_id: str) -> Skill:
        return self._skills[skill_id]

    def list_descriptors(self) -> list[SkillDescriptor]:
        return [skill.descriptor for skill in self._skills.values()]

    def clear(self) -> None:
        self._skills.clear()
