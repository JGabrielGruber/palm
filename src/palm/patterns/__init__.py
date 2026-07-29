"""
Concrete behavior patterns (Django-style apps).

Default install is truthful: dag, parallel, pipeline, wizard.
Intention stubs (etl) are not auto-loaded (ST-003 / SD-013).
"""

from palm.patterns._apps import (
    INSTALLED_PATTERNS,
    INTENTION_PATTERNS,
    autoload,
)

autoload()

__all__ = [
    "INSTALLED_PATTERNS",
    "INTENTION_PATTERNS",
    "autoload",
]
