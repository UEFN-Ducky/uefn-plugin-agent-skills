"""Self-check: the agent-skills pack reads the way UEFN Ducky reads it (no app needed)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "skills" / "agent-skills"
REFS = PACK / "references"


def _frontmatter(path: Path) -> dict:
    """Ducky's subset: top-level scalars plus one nested map; quoted values are JSON strings."""
    lines = path.read_text(encoding="utf-8").split("\n")
    assert lines[0] == "---", f"{path.name}: no frontmatter"
    meta: dict = {}
    nested: dict | None = None
    for line in lines[1:]:
        if line == "---":
            return meta
        key, _, raw = line.strip().partition(":")
        raw = raw.strip()
        value = json.loads(raw) if raw.startswith('"') else raw
        if line.startswith("  ") and nested is not None:
            nested[key] = value
        elif raw:
            nested = None
            meta[key] = value
        else:
            nested = meta[key] = {}
    raise AssertionError(f"{path.name}: unterminated frontmatter")


def _ref_ids() -> set[str]:
    return {p.stem for p in REFS.glob("*.md")}


def test_manifest_and_pack_name() -> None:
    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["id"] == "agent-skills"
    assert manifest["data_sharing"] is False
    meta = _frontmatter(PACK / "SKILL.md")
    assert meta["name"] == PACK.name
    assert meta["description"] and meta["license"] == "MIT"
    assert meta["metadata"]["source_plugin_id"] == manifest["id"]
    assert (PACK / "LICENSE.txt").read_text(encoding="utf-8").startswith("MIT License")


def test_every_reference_has_description_label_and_unique_order() -> None:
    orders: dict[int, str] = {}
    for path in sorted(REFS.glob("*.md")):
        meta = _frontmatter(path)
        assert meta.get("description"), path.name
        assert meta["metadata"].get("label"), path.name
        order = int(meta["metadata"]["order"])
        assert order not in orders, f"{path.name} and {orders[order]} share order {order}"
        orders[order] = path.name
    assert len(orders) == 42


def test_links_resolve_to_references() -> None:
    ids = _ref_ids()
    for path in [PACK / "SKILL.md", *REFS.glob("*.md")]:
        text = path.read_text(encoding="utf-8")
        assert "agent-skills:" not in text, path.name
        assert not re.search(r"\.\./(references|docs)/", text), path.name
        prefix = "references/" if path.name == "SKILL.md" else ""
        for target in re.findall(r"\]\(([^)#:]+\.md)(?:#[^)]*)?\)", text):
            assert target.startswith(prefix) and target[len(prefix):-3] in ids, f"{path.name}: {target}"
        for name in re.findall(rf"`{prefix}([a-z0-9-]+)\.md`", text):
            if name not in {"0004-title"}:  # an example ADR file name
                assert name in ids, f"{path.name}: {name}.md"


def test_router_names_only_existing_references() -> None:
    text = (PACK / "SKILL.md").read_text(encoding="utf-8")
    tree = text.split("```", 2)[1]
    named = set(re.findall(r"→ ([a-z-]+)", tree))
    named |= set(re.findall(r"^\| \w+ \| ([a-z-]+) \|", text, re.M))
    assert len(named) == 24
    assert named <= _ref_ids(), named - _ref_ids()
