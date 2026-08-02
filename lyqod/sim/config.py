"""SimConfig - the frozen, hasable description of one simulation scenario

Replaces ../psk's flat ``DEFAULT_PARAMS`` dict. Three things changed on purpose:

1. **Nested and typed.** Link budget, radar scene, modulation, and algorithm knobs
    are separated frozen dataclasses instead of 22 keys in one namespace
2. **Open for extension**: ``extra`` carries solver-specific knobs, so a new
    solver no longer has to edit a global defaults table to get its parameter
    pas validation (``make_params`` raised ``KeyError`` on unknown keys-
    ../psk/core/config.py:67)
3. **Hashable by content** ``fingerprint()`` is the basis of work-unit identity,
    so an unchanged scenario is never re-simulated.

Note ``Gamma`` and ``V`` are *not* here. Gamma is a scenario field (it defines
the radar QoD floor) and lives in ``SimConfig``; V is a solver knob and
belongs in the solver's params. Values that were ``None`` placeholders in
../psk (``T``, ``V``) are supplied by the experiment layer instead.
"""

from __future__ import annotations

import copy
from dataclasses import asdict, dataclass, field, replace
from typing import Any, Mapping

import numpy as np

from lyqod.store.hashing import canonical_json, content_hash
