# ADR-022: NeonRoot as a Palm provider (Sovereign Runners, 0.53)

## Status

**Accepted** — July 2026 (0.53.0 planning).  
Sibling of [ADR-003](003-provider-apps.md) (provider apps), [ADR-016](016-ci-gate.md) (NeonRoot CI).  
Planned in [VISION-0.53](../VISION-0.53.md). Docs **pipeline** dogfood is **[VISION-0.54](../VISION-0.54.md)**, not this ADR.

## Context

1. Palm extends outward through **providers** registered into the resource engine — never by teaching `palm.core` about REST, Postgres, or containers.
2. Project CI already chose **NeonRoot** for hermetic, local, git-seeded checks (ADR-016): `just ci-sandbox`, `palm-ci` image.
3. Living Library (0.52) produces `docs/_build/` via a thin stdlib builder; CSS still often needs Node/Tailwind on the host.
4. A future season wants Palm itself to **orchestrate** library builds and checks. Doing that by shelling `just` from a flow is **fake dogfood**. Doing that via a **neonroot provider** is real: isolation, images, and results become resources.

## Decision

1. **Add provider `neonroot`** under `palm/providers/neonroot/` as a standard ProviderApp (`name`, `actions`, `ready()`, registry registration).

2. **Actions (v0 minimum):** `health`, `spawn` (image + seed + command). Optional soon after: `image.ensure` / `list_images`.

3. **Optional dependency:** Palm must run without NeonRoot installed. Missing CLI → honest `health` failure / clear invoke error; do not pretend hermetic success. Prefer optional extra or experimental registration (PD-023 spirit).

4. **Seed policy:** default **`git-archive`** (clean tree) for hermetic claims; workspace path seed allowed but must be explicit in params (not silent).

5. **Tool images as phenotypes:** document `palm-ci` (exists), introduce or extend **`palm-docs`** (docs_build + CSS tooling) so host `docs/node_modules` is optional. Full-weight local workspaces remain supported.

6. **Scope boundary:** 0.53 = **runner capability**. 0.54 = **Palm pipeline** that composes runner steps into Living Library metabolism. Do not ship a “docs pipeline” that is only `subprocess(just)` under 0.53.

7. **No core pollution:** zero NeonRoot imports in `palm/core/`. Provider only.

## Consequences

- **Positive.** Hermetic execution becomes a catalogued resource; Assist/CLI/flows can request isolation without justfile exclusivity; 0.54 dogfood has real hands; workspace can thin out (tools in images).
- **Risk.** Flaky host/binary detection; CI without NeonRoot needs skip/mock policy. Mitigate with characterization tests and explicit skip markers.
- **Risk.** Scope creep into generic “any container runtime.” Rejected for 0.53 — NeonRoot first; other runners would be other providers.
- **Bounded.** Not a DocsService; not Cloudflare replacement; not mandatory install.

## Alternatives considered

- **Keep NeonRoot justfile-only.** Rejected — leaves isolation outside the product language and blocks honest 0.54 dogfood.
- **Generic `container` provider (Docker/Podman).** Deferred — wider surface, weaker fit to existing ADR-016 choice.
- **Docs pipeline in 0.53.** Rejected — runners first; pipeline second ([VISION-0.54](../VISION-0.54.md)).
- **Shell provider.** Rejected — unrestricted shell is not hermetic and breaks the isolation story.

## References

- [VISION-0.53](../VISION-0.53.md) · [VISION-0.54](../VISION-0.54.md) · [VISION-0.52](../VISION-0.52.md)  
- [ADR-016](016-ci-gate.md) · [ADR-003](003-provider-apps.md) · [PROVIDER-APPS.md](../PROVIDER-APPS.md)  
