# nuitka-project: --macos-create-app-bundle
# nuitka-project: --macos-app-name=teRMo
# nuitka-project: --macos-app-mode=ui-element
# nuitka-project: --product-name=teRMo
# nuitka-project: --macos-signed-app-name=net.cacko.termo
# nuitka-project: --macos-sign-identity=5D6C94808201B324ACB57431A017780BB494D9DC
# nuitka-project: --file-description=teRMo
# nuitka-project: --include-data-files={MAIN_DIRECTORY}/icon.png=data/icon.png
# nuitka-project: --macos-app-icon={MAIN_DIRECTORY}/icon.png
# nuitka-project: --macos-app-protected-resource="NSBluetoothAlwaysUsageDescription:b luetooth access"

from termo import start

if __name__ == "__main__":
    start()