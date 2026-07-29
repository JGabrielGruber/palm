"""Server-side rendering primitives — thin shared helpers for SSR surfaces."""

from palm.kits.server.ssr.layout import PALM_SSR_CSS, page_shell
from palm.kits.server.ssr.render import escape, html_response, pretty_json, redirect

__all__ = [
    "PALM_SSR_CSS",
    "escape",
    "html_response",
    "page_shell",
    "pretty_json",
    "redirect",
]
