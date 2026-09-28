"""Historical attendance transfer: ZKBioTime to Odoo."""
import sys
from datetime import datetime

import zk_odoo_sync as zk

START_DATE = "2025-01-01 00:00:00"

if __name__ == "__main__":
    zk.setup_logging("transfer")
    with zk.single_instance():
        errors = zk.run(datetime.strptime(START_DATE, zk.FMT), zk.now_local())
    sys.exit(1 if errors else 0)
