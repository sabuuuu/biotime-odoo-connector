"""Incremental attendance synchronization: ZKBioTime to Odoo."""
import os
import sys
from datetime import datetime, timedelta

import zk_odoo_sync as zk

# Days re-read on every run: covers PCs switched off (weekends, holidays) and offline terminals
LOOKBACK_HOURS = float(os.environ.get("SYNC_LOOKBACK_HOURS", "168"))

if __name__ == "__main__":
    zk.setup_logging("sync")
    with zk.single_instance():
        end = zk.now_local()
        start = end - timedelta(hours=LOOKBACK_HOURS)
        if zk.SYNC_START_DATE:  # never sync punches before the go-live date
            start = max(start, datetime.strptime(zk.SYNC_START_DATE, "%Y-%m-%d"))
        if start > end:
            zk.log.info("Synchronisation inactive avant le %s", zk.SYNC_START_DATE)
            sys.exit(0)
        try:
            errors = zk.run(start, end)
        except Exception:  # BioTime / Odoo unreachable (PC off the office network…): retried next run
            zk.log.exception("Synchronisation interrompue, nouvel essai au prochain passage")
            sys.exit(2)
    sys.exit(1 if errors else 0)
