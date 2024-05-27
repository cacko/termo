# nuitka-project: --macos-create-app-bundle
# nuitka-project: --macos-app-name=teRMo
# nuitka-project: --macos-app-mode=ui-element
# nuitka-project: --product-name=teRMo
# nuitka-project: --macos-signed-app-name=net.cacko.termo
# nuitka-project: --macos-sign-identity=5D6C94808201B324ACB57431A017780BB494D9DC
# nuitka-project: --file-description=teRMo
# nuitka-project: --include-data-files={MAIN_DIRECTORY}/icon.png=data/icon.png
# nuitka-project: --macos-app-icon={MAIN_DIRECTORY}/icon.png
# nuitka-project: --macos-app-protected-resource="NSLocalNetworkUsageDescription:b luetooth access"
# nuitka-project: --include-package=websockets
# nuitka-project: --file-version="1.0.1"
# nuitka-project: --product-version="1.0.1"
# nuitka-project: --macos-app-version="1.0.1"

from termo import start
from termo.core import check_pid, pid_file, show_alert
import os

if __name__ == "__main__":
    if check_pid():
        show_alert("teRMo already running.")
        exit(1)
    else:
        pid_file.write_text(f"{os.getpid()}")
        start() 