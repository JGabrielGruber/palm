"""Structure policy — DNA refuse vs declared membership (pure, 0.63.6).

Refuse tokens are structure law. Packaging seeds DNA; if membership still
carries a refused shape, admission must not green-bar the lie.
"""

from __future__ import annotations

from collections.abc import Iterable

from palm.core.assembly.definition import AssemblyDefinition

# Refuse tokens (closed vocabulary for floor; grow by theme)
REFUSE_SERVER_SURFACES = "server_surfaces"
REFUSE_HTTP_SERVER_SURFACES = "http_server_surfaces"
REFUSE_BACKGROUND_DRAIN = "background_drain"
REFUSE_PRODUCT_CATALOG_HOME = "product_catalog_home"


def refuse_violations(
    definition: AssemblyDefinition,
    *,
    surfaces: Iterable[str] = (),
    capabilities: Iterable[str] = (),
) -> tuple[str, ...]:
    """Return reason codes when membership violates DNA refuse.

    Empty tuple means policy holds. Reasons are stable strings for admission.
    ``work_drain`` membership is ``definition.capabilities``. *capabilities*
    is the leftover external bag (other organs still seed composition).
    """
    refuse = definition.refuse
    surfs = frozenset(str(s) for s in surfaces if s)
    reasons: list[str] = []

    if REFUSE_SERVER_SURFACES in refuse and surfs:
        reasons.append(f"refuse:{REFUSE_SERVER_SURFACES}")

    if REFUSE_HTTP_SERVER_SURFACES in refuse:
        httpish = surfs - {"mcp"}
        if httpish:
            reasons.append(f"refuse:{REFUSE_HTTP_SERVER_SURFACES}")

    # Dual name: refuse token ``background_drain`` vs capability ``work_drain``.
    # Membership is DNA capabilities, not the composition / option bag.
    if REFUSE_BACKGROUND_DRAIN in refuse and definition.has_capability("work_drain"):
        reasons.append(f"refuse:{REFUSE_BACKGROUND_DRAIN}")

    # product_catalog_home — floor: no composition signal yet; reserved token
    _ = REFUSE_PRODUCT_CATALOG_HOME

    return tuple(reasons)


__all__ = [
    "REFUSE_BACKGROUND_DRAIN",
    "REFUSE_HTTP_SERVER_SURFACES",
    "REFUSE_PRODUCT_CATALOG_HOME",
    "REFUSE_SERVER_SURFACES",
    "refuse_violations",
]
