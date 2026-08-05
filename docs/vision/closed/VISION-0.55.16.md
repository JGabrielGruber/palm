# VISION 0.55.16 — Kind-generic wait delivery

**Status:** ✅ **Done** (slice) — post-exit hardening after [VISION-0.55.15](VISION-0.55.15.md).  
**ADR:** [025-reactive-interests](../../adr/025-reactive-interests.md) — placement/extension, not new law.  
**Trigger:** Continue plane maturity report **P2** — `deliver.py` hardcodes nested wizard + `output_key`.

> *Plane delivers completion. Which shape is pluggable — not a special case forever.*

---

## 1. Problem

On positive match, `WaitPlaneService` always called `deliver_nested_wizard_completion`.  
That is honest for v1 nested jobs, but:

- workload / future kinds have no place to plug delivery
- `common/wait` knows nested wizard meta (`source`, `pattern_park`, `output_key`) as *the* deliverer
- next kind would fork `plane.resume_owner`

---

## 2. Intent

| Do | Outcome |
|----|---------|
| **Wait deliver registry** | Named deliverers + match predicates |
| Plane calls **`deliver_wait_completion`** | First matching deliverer that writes wins |
| Nested remains default deliverer | Same payload → `output_key` behavior |
| Register-downward friendly | Patterns/providers can register without editing plane |

### Non-goals

- Kill resource poll fallback (P3)  
- Host workplane peer (P4)  
- Workload product delivery (0.56 — register when ready)  
- Move nested source constant into pattern package (would invert common→pattern)  

---

## 3. API

```text
register_wait_deliverer(name, fn, *, matches=… | kind=… | source=…)
unregister_wait_deliverer(name)
deliver_wait_completion(owner_job, interest, get_job) -> bool

Default (import-time):
  nested_wizard → deliver_nested_wizard_completion
```

`fn(owner_job, interest, get_job) -> bool` — True if delivery wrote something material.

---

## 4. Success criteria

1. Plane has no direct nested import call site (uses registry façade).  
2. Nested dogfood / delivery tests green.  
3. Custom deliverer can register and run for a non-nested interest.  
4. Docs note the extension point for 0.56.

---

*Match continues the owner. Delivery shapes what the owner sees.* 🌴⚡
