# Intended package map

**Status:** Stub. Target layout — refine as the architecture vault grows.

| Area | Intended home (sketch) | Notes |
|------|------------------------|--------|
| Pure structure | `palm.core.assembly` | Reconciler + definition types |
| System structure | `palm.system.assembly` | Manager, seat, hands, seed |
| Boot | `palm.system.boot` | Machine up |
| Planes / supervisor | `palm.system.subsystems…` | Traffic and continuous care |
| Product | `palm.services…` | Userland |
| Surfaces | `palm.runtimes…` | Transport |
| Host | `palm.app.host…` | Wire / packaging |

Add one note per package family when boundaries need prose (`core.md`, `system.md`, …).
