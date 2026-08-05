# Palm — System log plan (0.59.1a)

**Status:** ✅ **Basic shipped** (theme **0.59** · slice **0.59.1a**). Grow verbosity with schedule migration.  
**Code:** `palm.system.log` · wired on `ApplicationHost.start` / `BaseRuntime.start`  
**Theme:** [VISION-0.59](vision/closed/VISION-0.59.md) · inventory [BOOT-INVENTORY](BOOT-INVENTORY.md) · [ADR-028](adr/028-system-boot.md) **Proposed**  
**Debt:** [BI-015](../TECH-DEBT.md#bi-015) · parent [SD-014](../TECH-DEBT.md#sd-014) · related [CS-002](../TECH-DEBT.md#cs-002)  
**Map:** [PALM.md](PALM.md) · event plane [EVENT-PLANE](EVENT-PLANE.md) · domain journal `palm.common.events.journal`  
**Language:** ASD-STE100 (practical).

---

## 1. Goal

Give Palm a **system log**: an ordered, human-readable narrative of **system life**.

Operators and agents must answer without reading source:

> What did Palm do, in order?  
> Where is it now?  
> What did it skip, and why?

This is **not** the domain event bus.  
This is **not** the domain event journal (redrive / projections).  
This is the Palm analog of **`journalctl` for Palm’s own boot and system path**.

### 1.1 Shipped in 0.59.1a

| Piece | Status |
|-------|--------|
| `SystemLog` ring + levels + phase helpers | ✅ |
| Console sink (stderr; quiet under pytest unless `PALM_SYSTEM_LOG=1`) | ✅ |
| Host + system boot phase lines (inventory-aligned ids) | ✅ |
| Skip reasons (surfaces, projections, work_drain, outbox, bind) | ✅ |
| `host.system_log` · doctor `event_plane.system_log_recent` | ✅ |
| Mode default levels (BootMode) · walker reuses phase API | ✅ 0.59.2 |
| Early seats `host.system_log` / `system.log.ready` | ✅ 0.59.2 |
| Mode dogfood applies levels on `for_mode("safe"|"test")` start | ✅ 0.59.6 |
| Shape dogfood applies levels on `for_mode("dev"|"prod"|…)` | ✅ 0.59.7 |
| Full operate catalog · JSON file sink · OTel | later |

---

## 2. Does this belong in 0.59?

**Yes — as a seat and a plan; implementation when convenient.**

| Question | Answer |
|----------|--------|
| Is system log the theme title? | **No.** Theme title is boot schedule + composition truth. |
| Does system log serve the theme? | **Yes.** Stub migrations break; you need sequence, not only inventory docs. |
| Does it replace the phase table? | **No.** The phase table is control. The system log is **observation**. |
| When to code? | Prefer **seat in 0.59.2** (walker can emit). Fill verbosity as phases migrate. Finish before theme exit if cheap; else residual **BI-015**. |

**Why it is not out of theme:**

1. Break/harvest needs a **tape**, not only BI rows written after the fact.  
2. Phase tables without emit are still opaque at runtime.  
3. Modes and membership skips must be **visible** (“skipped: composition has no journal”).  
4. Agents and humans debug the **same way** you use `journalctl` — ordered story first.

**Why we plan first (0.59.1a):**

- Avoid inventing a third bus or a fake full observability product.  
- Lock vocabulary so stubs do not log wrong things.  
- Allow partial ship without waiting for perfect telemetry.

---

## 3. Will this help agents (and humans)?

**Yes.**

| Without system log | With system log |
|--------------------|-----------------|
| Diff code + guess order | Read one ordered tail |
| Doctor = snapshot only | Snapshot **plus** recent sequence |
| “It failed” with no phase | `phase=host.product.wire failed: …` |
| Dual-bus confusion | System log names **schedule** and **bus** when relevant |
| Inventory is static | Live run matches inventory ids |

For coding agents mid-theme: system log is the **runtime form of BOOT-INVENTORY**.  
For you on Linux: same reason you open `journalctl` — causal tape after a break.

---

## 4. Three tools (do not merge)

| Tool | Job | Palm today | Target |
|------|-----|------------|--------|
| **System log** | Ordered narrative of boot / mode / plane / membership / fail | Missing / sparse stdout | **This plan** |
| **Event bus** (`EventEngine` ×2) | Live reaction (start / continue) | Strong | Unchanged law |
| **Domain journal** (`EventJournal`) | Durable selected domain facts + consumer offsets | Exists; allowlist | Unchanged job |

**Law:**

- Reaction stays on **`runtime.event`** / **`host.event`** as today ([EVENT-PLANE](EVENT-PLANE.md)).  
- Domain redrive stays on **EventJournal**.  
- System log may **mirror** important facts as text; it must **not** become the wait/work path.  
- Do not collapse doctor status names by inventing a fourth vocabulary (see CS-002). Prefer **one system-log lexicon** + thin doctor pointers.

---

## 5. Verbosity — how alive can Palm feel?

Use **levels**. Default for `dev` is rich. Default for `test`/`safe` is lean (deterministic, low noise).

### 5.1 Levels

| Level | Intent | Feel |
|-------|--------|------|
| **0 quiet** | Almost off (prod opt-in) | Errors only |
| **1 lifecycle** | Boot story | Palm wakes, walks phases, ready or fails |
| **2 system** | + planes, ports, membership | You know *what* attached and *what* skipped |
| **3 operate** | + recover, drain, surface mount | Dogfood “alive” without job spam |
| **4 detail** | + selected domain highlights | Optional bridge lines (not every BT tick) |
| **5 trace** | Dev only | Handler enter/exit; rare |

**Recommended defaults (modes):**

| Mode | Default level |
|------|----------------|
| **safe** | 1 |
| **test** | 1 (or 0 in tight unit tests) |
| **dev** | 3 |
| **prod** | 1 (raise on incident) |
| **cli one-shot** | 2 if TTY; 1 if quiet flag |

### 5.2 What makes it feel “alive”

Write lines as **state descriptions**, not code dumps.

Good:

```text
[palm] host boot mode=dev composition=all_in_one
[palm] host phase host.kernel.bootstrap start
[palm] plugins ensure ok patterns=wizard,linear providers=kv
[palm] system main schedule start
[palm] system phase system.planes.attach wait=on session=on workload=stub
[palm] host phase host.product.wire services=definitions,execution,session,assist
[palm] capability journal skip reason=composition_off
[palm] host phase host.ready ok duration_ms=412
[palm] work_drain background start
```

Bad (avoid as primary voice):

```text
DEBUG ApplicationHost.start line 640
calling _wire_cqrs
```

**Alive** means: a reader can sketch Palm’s phenotype from the last 30 lines.

### 5.3 Verbosity budget (anti-spam)

| Always allow (at level ≥1) | Never default |
|----------------------------|---------------|
| Phase start / end / skip / fail | Every BT tick |
| Mode + composition + deployment ids | Full payload dumps with secrets |
| Plane attach / detach | Per-state-key writes |
| Membership skip with reason | Every event-bus publish |
| Recover summary | Per-handler stack without error |
| One line at host ready | Duplicate host + system spam for same fact |

Domain job noise stays on the **event plane** and optional journal.  
System log may emit **one** line at job terminal if level ≥4 (`job j-… SUCCEEDED flow=…`) — not a second orchestration bus.

### 5.4 Message shape (stable fields)

Prefer structured fields + a short human `message`:

| Field | Example |
|-------|---------|
| `ts` | ISO-8601 UTC |
| `level` | info / warn / error |
| `component` | `host` \| `system` \| `plane` \| `composition` \| `mode` |
| `schedule` | `host` \| `system` |
| `phase` | provisional id from [BOOT-INVENTORY](BOOT-INVENTORY.md) |
| `event` | `phase.start` \| `phase.end` \| `phase.skip` \| `phase.fail` \| `ready` \| … |
| `mode` | `dev` |
| `system_id` / `runtime` | `main` |
| `duration_ms` | end lines |
| `reason` | skip / fail |
| `message` | one human sentence |

Render for console:

```text
2026-08-01T12:00:00Z INFO host phase.end phase=host.ready duration_ms=412 — host ready mode=dev
```

JSON line form optional (`PALM_SYSTEM_LOG_FORMAT=json|console`).

---

## 6. What to log (catalog)

### 6.1 Must (lifecycle / boot — level 1+)

| When | `event` | Notes |
|------|---------|--------|
| Boot begins | `boot.start` | mode, composition, deployment |
| Each phase enter | `phase.start` | schedule + phase id |
| Phase skip | `phase.skip` | **reason** required |
| Phase fail | `phase.fail` | reason + short error class |
| Phase ok | `phase.end` | duration_ms |
| Host / system ready | `ready` | |
| Shutdown | `shutdown.start` / `shutdown.end` | |

Phase ids track the boot table (inventory → stubs → real handlers).

### 6.2 Should (system feel — level 2–3)

| When | Notes |
|------|--------|
| Plugin ensure | count / notable names, not full dump |
| Port open | execution / … |
| Plane attach | wait, session, work, workload — on/off |
| Membership decision | service/surface/capability included or skipped |
| Dual root | `ServerContext` vs host — name the path |
| Recover summary | rebuilt N, lag, workers ready |
| Background start/stop | work_drain |

### 6.3 May (operate bridge — level 4)

| When | Notes |
|------|--------|
| WorkIntent enqueue/succeed/fail | one line; domain journal still owns durable truth |
| Job terminal | one line; no step spam |
| Surface listen | host:port |

### 6.4 Never as system log spam

- Per-node BT evaluation  
- Per-state set without opt-in  
- Full definition JSON  
- Secrets, tokens, full user answers  

---

## 7. Sink and API (implementation intent)

### 7.1 Package home

| Piece | Home |
|-------|------|
| Record + ring + phase API | `palm.system.log` |
| Host wire | `ApplicationHost.start` / `shutdown` |
| System wire | `BaseRuntime.start` / `stop` |
| Doctor tail | `HostObservability.event_plane_status` → `system_log_recent` |

### 7.2 Sinks (v1 shipped)

| Sink | Role |
|------|------|
| **stderr** | When `console=True` (default outside pytest; `PALM_SYSTEM_LOG=1` forces on) |
| **In-memory ring** | Last N (`PALM_SYSTEM_LOG_CAPACITY`, default 200) |
| **Env level** | `PALM_SYSTEM_LOG_LEVEL` = 0…5 or name (`lifecycle`, `operate`, …) |

No new durable store. OS journald still wraps the process.

### 7.3 API (code)

```python
from palm.system.log import get_system_log, configure_system_log

log = get_system_log()
log.info("boot.start", "host boot start", schedule="host")
with log.phase("host", "host.product.wire"):
    ...
log.phase_skip("host", "host.surfaces.mount", reason="deployment.server_off")
host.system_log.recent(limit=20)
```

Walker (0.59.2+) should call the same helpers so migration does not invent a second path.

### 7.4 Relation to stdlib `logging`

- Ad-hoc module loggers stay for local noise.  
- **Boot story goes through SystemLog.**  
- Optional bridge to `logging.getLogger("palm.system")` later if useful.

---

## 8. Ordered work inside 0.59

| When | Work | Result |
|------|------|--------|
| **0.59.1a** | Plan **+** basic implement | ✅ ring, console, host+system phase lines |
| **0.59.2** | Walker reuses SystemLog phase API · mode levels | ✅ No dual narrative |
| **0.59.3+** | Full schedule walk emits phase lines only via SystemLog | cutover |
| **Membership** | More skip reasons | Composition visible |
| **Theme exit** | BI-015 closed or residual | OPS note if needed |

---

## 9. Tests and green bar

| Test | Intent |
|------|--------|
| Unit | ring retains N; skip requires reason |
| Boot characterization | host start in `test` mode produces phase.start…ready sequence |
| Quiet mode | `safe`/`test` default does not flood |
| No reaction law break | system log does not resume jobs or enqueue work |

Spine green bar does **not** require level 3.  
Level 1 sequence on collapsed host **should** become part of characterization when seats exist.

---

## 10. Non-goals (this plan)

| Out | Why |
|-----|-----|
| Full OpenTelemetry product | Later; narrative first |
| Replace EventJournal | Different job |
| Merge host + runtime buses | Breaks reactive law |
| Log every domain event by default | Spam; wrong tool |
| Require durable disk for v1 | stderr + ring enough |
| Unify CS-002 three status JSON shapes in this plan | Optional later; system log is sequence |

---

## 11. Success criteria

- [x] Written law: system log ≠ bus ≠ domain journal (this file).  
- [x] Console + ring buffer; doctor / `host.system_log` can read recent lines.  
- [x] Phase start/end/skip/fail with human `message` on host + system start.  
- [ ] Mode-based default levels (with boot modes).  
- [x] A cold reader can describe phenotype from a host boot tail (tests).  
- [ ] BI-015 closed or residual named at 0.59 exit.  
- [x] No secrets; no BT tick flood.

---

## 12. Answers (record)

**Does this make sense for properly doing 0.59?**  
Yes. It is observation for the control work of boot. Plan now; seat early; finish when phases land.

**Will it help agents?**  
Yes. Ordered tape + inventory ids reduce “read the source to know boot order.”

**How verbose for “coming to life”?**  
Default **dev = level 3** (lifecycle + planes + membership + recover/drain).  
That is enough to feel alive. Level 4 is optional bridge. Level 5 is rare.

---

## 13. How to update this file

- Mark implementation slices with ✅ and patch id.  
- Keep catalog in sync with phase ids when BOOT-INVENTORY locks.  
- At theme exit: link OPS/PALM if shipped; else residual BI-015.  
- Do not paste full event-plane law — link [EVENT-PLANE](EVENT-PLANE.md).
