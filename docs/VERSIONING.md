# Palm — Versioning & Release Convention

**Status:** canonical (established 0.46.0 · **theme discipline** clarified **0.61.0**). Applies to all future work.

Palm had a *de-facto* cadence (0.45.1 → 0.45.8, one feature per patch) but no written rule. This document is
that rule. It is referenced by `AGENTS.md` (docs + themes) and the review checklist.

**Also see:** [AGENTS.md](../AGENTS.md) (agent rules) · [WRITING.md](WRITING.md) (VISION text) · [PHILOSOPHY.md](../PHILOSOPHY.md) (spirit).

---

## Scheme: `0.MINOR.PATCH` (pre-1.0)

Palm is pre-1.0, so the SemVer `MAJOR` slot stays `0` and stability guarantees are relaxed:

- **MINOR (`0.X`) = a theme.** One coherent arc of work — a capability, or a consolidation/debt goal. A minor
  **may** introduce breaking changes; when it does it ships a `MIGRATION-0.X.md`.
- **PATCH (`0.X.N`) = one shippable slice** within the theme — a single feature or tracked work-item (e.g. a
  `TECH-DEBT.md` row). One focused change per patch **when possible**.

> **Release cadence — embedded release.** Each slice is its own *commit*, but the **version is not bumped per
> commit** (every bump restamps 6+ doc surfaces — needless churn). We cut an **embedded release** — the
> `just bump-version` + `CHANGELOG` + doc-sync — per **minor or per patch-group**, grouping several slice-commits
> under one released version. Small steps in git; releases in batches. This is the organic palm flow.

> At **1.0** we switch to strict SemVer (MAJOR = breaking, MINOR = additive, PATCH = fix).

---

## Theme discipline (ambition over empty process)

Themes exist so Palm **grows properly** — one coherent intent, honest debt, layer law.  
Process that **kills ambition** or forces dual-truth workarounds is **wrong process**. Fix the rule; do not shrink the organism.

### Who decides (sole human authority)

Palm is a **single-human** project for product and theme authority.

| Role | Person | What they decide |
|------|--------|------------------|
| **Technical lead / owner** | **José Gabriel Gruber** (**José**) | Theme open/close; floor vs growth; when exit is proper; ambition vs process; ADR accept at exit; residual debt that stays named |

**Agents and collaborators propose.** They plan slices, implement, and argue for proper homes.  
They do **not** close a theme, shrink ambition to “finish process,” or treat a VISION checklist as José’s decision.

When docs say **exit judgment**, **theme stays open**, or **ambition over process** — that is **José’s call** to make tangible in negotiation. Ask him. Do not invent a committee or a silent agent exit.

### Floor, growth, exit

| Concept | Meaning |
|---------|---------|
| **Floor** | Minimum bar to claim the theme’s *intent is real* (e.g. “eyes open”). A **floor**, not a coffin. |
| **Growth line** | Work that may continue under the **same** minor while the theme stays open. Slices may merge, split, or extend. |
| **Exit** | **José’s judgment** when the home is proper, residual is honest, and declared green bars hold. |

**Exit is not:** ticking every seed table row, killing the theme because a checklist looks complete, or shipping a lie so the minor can close on schedule.

**Exit is:** the intent holds in code and docs; ADR Accepted (or waived honestly); residual debt **named**; spine green on declared modes; **José says the theme may close**.

### Prefer / reject (planning and execute)

| Prefer | Reject |
|--------|--------|
| **Proper** homes, lexicon, and discovery | Workarounds that “ship thin” by lying or dual truth |
| **Break ugly** paths; pay debt if feasible; else **name** it | Keep dual paths because tests freeze old JSON |
| **Big work** when the home is wrong | Fear of large renames / deletes that unblock growth |
| **Theme stays open** while intent is unfinished | Kill-theme theater for empty notes |
| Safety that protects **layer law** (core purity, ports, no second start/continue) | Process rules that shrink Palm’s prospect |
| Slice table as a **guide** | Slice table as a sealed contract that forbids needed work |
| Compress *paperwork* | Compress *ambition* to fit a short exit story |

### Non-goals vs forever bans

| Kind | Meaning |
|------|---------|
| **Not this theme’s subject** | Another seed may own it later — not “forbidden forever.” |
| **Forbidden always** | Layer law: e.g. no second start/continue path; no silent Design mutation; no fake green for absent seats. |

Do not write VISION “non-goals” that permanently ban growth Palm will need.  
Do write clear **layer forbidden** lists that protect truth.

### Workarounds

If implementing the theme would require a **permanent** workaround:

1. **Break** the underlying shape, or  
2. **Open a debt row** with owner and residual honesty, or  
3. **Do not claim** that part of the theme.

Do **not** ship the workaround as the architecture of record.

### Slices

- Prefer **one purpose** per slice-commit (`feat(0.X.N): …`).  
- Sub-slices (`0.X.Nb`) and **merge of tiny slices** are fine when review stays clear.  
- **Extend** the theme with `0.X.N+` growth slices without reopening a seed file if the home is the same.  
- Numbered tables in VISION are **ordered intent**, not a death clock.

### The `X.0` planning release

`0.X.0` **opens** a minor. It carries the *plan*, not features:

- Adds `docs/VISION-0.X.md` — goal, **floor + growth**, non-goals that are real, principles, homes, **guide** slice table, debt budget.  
- Adds/updates ADR(s) for structural decisions (status **Proposed** until exit).  
- Names debt the theme will pay or leave residual.  
- Execution starts at `0.X.1`.

**Rhythm per theme:** `0.X.0` plan → `0.X.1 … 0.X.N` execute → **exit when José judges proper** → open `0.(X+1).0` when the next arc starts.

---

## Artifacts by level

**Per minor (`0.X`)**
- `docs/VISION-0.X.md` — **required** (the plan; floor + growth + exit judgment)
- `MIGRATION-0.X.md` — **required iff** the theme breaks API/contracts
- ADR(s) for significant structural decisions
- `STATUS.md` updated; `CHANGELOG.md` section

**Per slice-commit**
- Commit `feat(0.X.N): <summary>` (or `fix(0.X.N):` / `refactor(0.X.N):`) — **keep the patch id** as the logical slice label; a `b`/`c` suffix is fine for sub-slices (e.g. `0.47.5c`). One focused change when possible; cite the tracked item. **No `just bump-version`** — the codebase version advances only at the embedded release.
- **Green `just check`** / `just ci` (lint + test + guards) — enforced in CI for the declared green bar of that slice.

**Per embedded release (a minor or a patch-group)**
- `just bump-version 0.X.N` — once, covering the grouped slice-commits (version + doc-surface sync).
- `CHANGELOG.md` entry summarizing the group; `STATUS.md` updated.

## Version sources of truth & bump flow

Two files hold the version, kept in lockstep by `scripts/version_utils.py`:
- `pyproject.toml` `[project].version`
- `src/palm/__init__.py` `__version__`

Bump with (**at an embedded-release point — a minor or patch-group — not per commit**):

```
just bump-version 0.X.N        # → scripts/sync_version.py --set
```

This propagates the stamp to the **auto-synced** surfaces: `README.md`, `STATUS.md`, `ARCHITECTURE.md`,
`DEVELOPMENT.md`, `SCOPE.md`, `docs/llms.txt`, `docs/mcp.txt`, `docs/DOCKER.md`, `docs/index.html`, plus
MCP/Grok **doc mirrors** ([0.52.1](vision/closed/VISION-0.52.md)). Verify with `uv run python scripts/sync_version.py --check`
and `just docs-check`.

## Publishing

Publishing to PyPI is at maintainer discretion — not every patch must publish, and `X.0` planning releases are
typically not published. Release gate: `just release-prep` (docs-check + full-check + build). See
`DEVELOPMENT.md` → "Release & publishing".

## Current program — themes and debt (0.46+)

Themes sequence by **intent and dependency**, not by rigid T-number order alone.  
`TECH-DEBT.md` is the live ledger; pay or name residual when a theme moves.  
Security / one-line quick-wins may land early regardless of theme.  
See also [VISION-0.61](vision/closed/VISION-0.61.md) for a theme that states floor vs growth explicitly.
