"""Incremental attendance synchronization: ZKBioTime to Odoo."""
import sys
from datetime import datetime, timedelta

import zk_odoo_sync as zk

LOOKBACK_HOURS = 72

if __name__ == "__main__":
    zk.setup_logging("sync")
    with zk.single_instance():
        end = zk.now_local()
        start = end - timedelta(hours=LOOKBACK_HOURS)
        if zk.SYNC_START_DATE:  # never sync punches before the go-live date
            start = max(start, datetime.strptime(zk.SYNC_START_DATE, "%Y-%m-%d"))
        errors = zk.run(start, end)
    sys.exit(1 if errors else 0)
