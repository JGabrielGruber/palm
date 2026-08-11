# Glossary — intended architecture

**Status:** Stub. Engineering terms only. One meaning per term.  
**Metaphor / teaching words:** [appendix/metaphor.md](appendix/metaphor.md).

| Term | Intended meaning | Do not use for |
|------|------------------|----------------|
| **Core** | Pure engines and pure types (`palm.core`) | Host packaging |
| **System** | Running organism: seats, ports, planes, boot | Product business rules |
| **Product** | Userland services (assist, flows façades, …) | Transport adapters |
| **Surface** | Transport edge (`palm.runtimes`) | Structure law |
| **Host** | Composition root — wire once | Public structure API for product |
| **Port** | Named effect interface on the shell | HTTP “port” number (say *network port*) |
| **Plane** | System path for a kind of traffic | Deployment “plane” |
| **Structure definition** | Declarative desired structure for a process | Business flow definition |
| **Structure reconciler** | Pure engine: definition + observations → status + intents | Job orchestration |
| **Structure manager** | System loop that materializes structure and publishes readiness | Admission-only dashboard |
| **Admission** | Published gate: may business that needs ground run? | Authn/authz |
| **Composition** | Capability membership of a process | Docker Compose product name |
| **Place book** | Named places (workload / bodies) | Business catalog |
| **Job path** | Definition → pattern → job → effects → events | Structure assemble path |

Add rows when a note needs a stable name. Prefer [PALM.md §3](../PALM.md) when a term already lives there — link, do not fork forever.
