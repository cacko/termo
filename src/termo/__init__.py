__name__ = "jobs"
__version__ = "0.2.11"

import corelog
import os


corelog.register(os.environ.get("TERMO_LOG_LEVEL", "INFO"))
