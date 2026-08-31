"""DEPRECATED shim — this module is now `magnet.log`.

The word "ledger" is retired (house ruling: use LOG, record, or database). This
module re-exports `magnet.log` so any existing import keeps working, and warns
once. It will be removed after the Sep-14 submission.
"""
import warnings

from magnet.log import *  # noqa: F401,F403
from magnet.log import (  # noqa: F401  explicit re-export of the private-ish names
    DEFAULT_LOG,
    LEGACY_LOG,
    SCHEMA,
    adopt_change,
    connect,
    default_log_path,
    ensure_schema,
    get_demo_bonus,
    latest_adoption,
    list_readings,
    migrate_legacy_database,
    record_reading,
    record_week,
    reset_demo,
    set_demo_bonus,
)

warnings.warn(
    "magnet.ledger is deprecated; import from magnet.log instead",
    DeprecationWarning,
    stacklevel=2,
)
