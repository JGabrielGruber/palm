# Session plane (concept)

**Status:** Living · theme [VISION-0.58](../../VISION-0.58.md) · map [PALM.md](../../PALM.md) · ADR [027](../../adr/027-session-plane.md)

## One idea

**Session** is the **outside subject** and system glue. It is **not** one flow run.

| Term | Meaning |
|------|---------|
| **`session_id`** | System subject (`sess-…` or service `sess-svc-…`) |
| **`instance_id`** | Product continue handle for one run |
| **BoundSurface** | Surface bind: system session + continue instance |
| **SessionService** | Product door (not the wait plane) |

One session may own **many** instances. **Active** is focus only. Continue uses the **wait plane**. Dual-own is forbidden.

## Paths agents see

| Kind | Shape |
|------|--------|
| Product continue | `/v1/api/…/instance/{instance_id}` · segment `instance` |
| System journey | `system/session/{session_id}/…` |
| Soft land | Legacy segment `session` may parse; prefer `instance` |

## Where to learn more

- Agent skill: `docs/skills/palm/references/session-management.md`
- Operator guide: `docs/mcp.txt` · card `docs/mcp-card.txt`
- Full MCP inventory: [MCP.md](../../MCP.md)
