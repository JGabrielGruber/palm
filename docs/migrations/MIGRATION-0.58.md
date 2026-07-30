# Migration — 0.58 Session plane

**Theme:** [VISION-0.58](../VISION-0.58.md) (**closed**) · **ADR:** [027](../adr/027-session-plane.md) **Accepted**  
**Map:** [PALM.md](../PALM.md) · **Release:** [RELEASE-0.58.20](../releases/RELEASE-0.58.20.md)

Palm is pre-1.0. This theme **breaks the product lie** that `session_id` ≡ `instance_id`. Soft-land remains for some path segments and MCP params; do not rely on it forever.

## Breaking — vocabulary

| Was | Use instead |
|-----|-------------|
| `session_id` meaning the flow continue handle | **`instance_id`** for continue; **`session_id`** only for system subject (`sess-…`) |
| Product path segment `…/session/{id}` (emit) | **`…/instance/{instance_id}`** (legacy segment `session` may still **parse**) |
| REST assist/flows under `/session/` | `/v1/api/assist/instance/{instance_id}/…` · `/v1/api/flows/{flow}/instance/{instance_id}/…` |
| Dual names `system_session_id` / `palm_session_id` | Single system field **`session_id`** on plane/job meta when system-shaped |

## Breaking — attribution

| Was | Now |
|-----|-----|
| Bare instance continue with no owner | **Strict attribution** (default): continue needs owner (bound session or reverse index); bare orphan refuse. Compat: `PALM_SESSION_STRICT_ATTRIBUTION=false` |
| Start without system session when plane ready | Start always sessioned (bind/create or service session) |

## Product guidance

| Goal | Call |
|------|------|
| Bind outside subject | **SessionService** / kit `resolve_session_service` → **BoundSurface** |
| Continue a walk | `instance_id` (+ optional system `session_id` for gate) |
| Focus / list waiting / cancel owned | Session operate / `system/session/{id}/…` |
| Resume parked work | **Wait plane** only — not session private hooks |
| Agent operate | Prefer **`palm_assist`**; skill teaches session ≠ instance |

## Not broken by 0.58

| Area | Note |
|------|------|
| Wait / work / workload law | Unchanged verbs; session attributes start and owner |
| System journey paths | `system/session/{id}` remains system (not renamed to instance) |
| Class names `FlowSession` / `AssistSession` | May still exist as thin handles (**SI-002** residual) |

## Residual after theme close

| Open | Kind |
|------|------|
| **SI-002** / **SI-006** / **SI-007** / **SI-010** / **SI-016** | Residual honesty — see TECH-DEBT |
| **SU-*** surface weight / explorer / MCP dual stack | Optional; [VISION-SURFACE-DEFLATION](../VISION-SURFACE-DEFLATION.md) |
| **SD-014** boot phases | Later theme |
| User plane impersonation | Later (ADR-027 D11) |
