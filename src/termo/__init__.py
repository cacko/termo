__name__ = "termo"
__version__ = "0.0.1"

import logging
from pathlib import Path
import traceback
import corelog
import os
import sys
from termo.ui.app import TermoApp
import signal


corelog.register(os.environ.get("TERMO_LOG_LEVEL", "INFO"))

def start():
    try:
        app = TermoApp()

        def handler_stop_signals(signum, frame):
            app.terminate()
            sys.exit(0)

        signal.signal(signal.SIGINT, handler_stop_signals)
        signal.signal(signal.SIGTERM, handler_stop_signals)
        app.run()
        app.terminate()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        with Path("/tmp/termo.log").open("a") as fp:
            fp.writelines(traceback.format_exc())
        logging.exception(e)
