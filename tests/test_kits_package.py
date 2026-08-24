"""Smoke tests for palm.kits install truth."""

from __future__ import annotations


def test_installed_kits_include_server() -> None:
    from palm.kits import INSTALLED_KITS, get_kit, list_kits

    assert "server" in INSTALLED_KITS
    info = get_kit("server")
    assert info is not None
    assert info.module == "palm.kits.server"
    names = {k.name for k in list_kits()}
    assert "server" in names


def test_server_kit_protocol_exports() -> None:
    from palm.kits.server import ServerRequest, ServerResponse, transport_registry

    assert ServerRequest is not None
    assert ServerResponse is not None
    assert transport_registry is not None


def test_common_runtimes_no_longer_hosts_server_kit() -> None:
    import importlib.util

    assert importlib.util.find_spec("palm.common.runtimes") is None
