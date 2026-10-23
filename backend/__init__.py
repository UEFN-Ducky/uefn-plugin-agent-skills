"""Agent Skills — Store desktop plugin (bundles the agent-skills skill pack)."""

from __future__ import annotations


def register(api) -> None:
    """Skill-only pack: no MCP tools; register marks the plugin loaded."""
    api.log("agent-skills skill plugin registered")
