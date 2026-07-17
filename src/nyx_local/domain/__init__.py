"""Domain package for future business concepts."""

from nyx_local.domain.memory import MemoryEntry, MemoryProvider
from nyx_local.domain.processes import ProcessInfo, ProcessProvider
from nyx_local.domain.skills import Skill, SkillDescriptor, SkillError, SkillRegistry, SkillResult

__all__ = [
    "MemoryEntry",
    "MemoryProvider",
    "ProcessInfo",
    "ProcessProvider",
    "Skill",
    "SkillDescriptor",
    "SkillError",
    "SkillRegistry",
    "SkillResult",
]
