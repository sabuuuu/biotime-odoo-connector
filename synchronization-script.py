"""Incremental attendance synchronization: ZKBioTime to Odoo."""
import sys
from datetime import timedelta

import zk_odoo_sync as zk

LOOKBACK_HOURS = 72

if __name__ == "__main__":
    zk.setup_logging("sync")
    with zk.single_instance():
        end = zk.now_local()
        errors = zk.run(end - timedelta(hours=LOOKBACK_HOURS), end)
    sys.exit(1 if errors else 0)
