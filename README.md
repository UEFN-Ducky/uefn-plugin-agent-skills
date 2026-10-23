# Agent Skills

Open-source [UEFN-Ducky](https://github.com/UEFN-Ducky/UEFN-Ducky) Store plugin that brings [Addy Osmani's Agent Skills](https://github.com/addyosmani/agent-skills) to UEFN Ducky: production-grade engineering workflows for coding agents, from spec to ship.

Desktop plugin id `agent-skills`. Install or update from **Settings → Store** in the app — do not install from a zip by hand.

## What it does

One skill pack, `agent-skills`, that every agent in UEFN Ducky can load (and that Ducky also deploys to Claude Code, Codex and the other coding agents it hooks up). No tools, settings or keys.

- **24 skills** by development phase: interview-me, idea-refine, spec-driven, constraint-driven, planning and task breakdown, incremental implementation, source-driven, doubt-driven, context engineering, frontend UI, API and interface design, test-driven development, browser testing with DevTools, debugging and error recovery, code review, code simplification, security and hardening, performance, git workflow, CI/CD, deprecation and migration, documentation and ADRs, observability, shipping and launch.
- **The router** (`SKILL.md`): which skill fits the task, the core operating behaviours (surface assumptions, push back, keep it simple, stay in scope, verify) and the lifecycle order. It also maps the skills' Claude Code steps to UEFN Ducky (terminals, Verse builds and tests, the Browser tab, helper chats).
- **Commands**: /spec, /plan, /build, /test, /review, /code-simplify, /ship, /webperf and /constraints as steps an agent follows when you type them.
- **Personas**: code reviewer, security auditor, test engineer and web performance auditor.
- **Checklists**: definition of done, testing patterns, security, performance, accessibility, observability and orchestration patterns.

## Layout

UEFN Ducky reads a skill pack as `SKILL.md` plus one flat `references/` folder, so the upstream repo is ported like this (from upstream 0.6.13, commit `aeac41d`):

| Upstream | Here (`skills/agent-skills/`) |
|----------|-------------------------------|
| `skills/using-agent-skills/SKILL.md` | `SKILL.md` |
| `skills/<name>/SKILL.md` | `references/<name>.md` |
| `agents/<persona>.md` | `references/<persona>.md` |
| `references/<checklist>.md` | `references/<checklist>.md` |
| `skills/idea-refine/{frameworks,refinement-criteria,examples}.md` | `references/idea-refine-{frameworks,criteria,examples}.md` |
| `skills/*/references/<file>.md` | `references/<file>.md` |
| `.claude/commands/*.md` | `references/commands.md`, one section per command |

Links between files point at the sibling reference (`hardening-patterns.md#injection`). Upstream's hooks, evals, docs and the idea-refine shell script are not shipped.

## Build

```bash
py scripts/build_zip.py
py scripts/release.py --publish --changelog "…"   # commit + push, zip, upload, publish to the Store
```

`build_zip.py` writes `deploy/agent-skills-<version>.ducky-plugin.zip` (scripts/, deploy/ and the self-check are not packed).

## Test

```bash
py -m pytest -q --import-mode=importlib backend/test_agent_skills.py
```

Checks the pack the way UEFN Ducky reads it: frontmatter on every file, every link and skill name resolving to a reference.

## License

MIT. The skill content is Copyright (c) 2025 Addy Osmani, MIT ([skills/agent-skills/LICENSE.txt](skills/agent-skills/LICENSE.txt)). The plugin wrapper is Copyright (c) 2026 Mindful Path Company, LLC ([LICENSE](LICENSE)). This plugin is not affiliated with Addy Osmani.
