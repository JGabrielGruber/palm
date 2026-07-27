# ADR-023: Hermetic jobs — NeonRoot as job runner, Palm as graph (0.54 replan)

## Status

**Accepted** — July 2026 (0.54.0 **replan**).  
**Supersedes** the earlier “library pipeline / DocsService in 0.54” framing of ADR-023 drafts.  
Sibling of [ADR-022](022-neonroot-provider.md). Docs product domain deferred past [VISION-0.55](../VISION-0.55.md) Reactive Interests and workload/session foundations.

## Context

0.53 delivered NeonRoot as a Palm provider (`health`, `spawn`, seed exclude, host `--output`) and tool images (`palm-ci`, `palm-docs`). NeonRoot workspaces are **tmpfs** (fast, disposable) with optional vault commit.

An intermediate 0.54 implementation put Living Library product logic in `common.library`, a `library` provider, and DocsService. That risked:

- domain product in the middle layer  
- hard-coded corpora instead of definition-driven process  
- under-investing in **DAG** (still a placeholder) and general hermetic job orchestration  

Palm’s purpose test is: **business rules as definitions; foreign code only in isolated runners.**

## Decision

1. **0.54 theme = hermetic jobs + definition graphs**, not docs CMS.

2. **NeonRoot** is the execution place for tool/code jobs (images, tmpfs workspace, spawn/output). Palm stores **job handles and outcomes**, not workspace trees.

3. **Palm graphs** (wizard resource chains now; **dag pattern** as the platform growth target) schedule resource nodes. Simple nodes use existing providers (kv, file, transforms); heavy nodes use **neonroot**.

4. **No domain library stack in 0.54.** Discard `common.library`, `providers/library`, `services/docs` from the 0.54 experiment. Optional Living Library **product** returns in a **later** minor after reactive interests + session/workload foundations.

5. **Security:** allowlists and policy for images/paths/commands may be hardcoded; **process structure** should be definitions.

6. **Palm may stage a run directory** under `data_dir` for bind-mode cooperation later; default remains spawn seed to tmpfs (cheap). Product pins (if any later) are explicit promote, not “left in the box.”

## Consequences

- **Positive.** Clear purpose test; core stays general; 0.53 investment preserved; DAG becomes first-class work.
- **Risk.** Docs product delayed — accepted; 0.52/0.53 static docs tooling remains.
- **Bounded.** Not a full artifact registry in 0.54; not multi-cluster vault sharing.

## Alternatives considered

- **Continue storage-backed DocsService in 0.54.** Rejected for now — too much product, too little platform proof.
- **Execute Python inside Palm.** Rejected — purity and security.
- **Whole-tree sync as default.** Rejected — prefer explicit outputs and disposable tmpfs.

## References

- [VISION-0.54](../VISION-0.54.md) · [VISION-0.55](../VISION-0.55.md) · [VISION-0.53](../VISION-0.53.md) · [ADR-022](022-neonroot-provider.md)  
