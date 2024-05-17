# nuitka-project: --macos-create-app-bundle
# nuitka-project: --macos-app-name=teRMo
# nuitka-project: --product-name=teRMo
# nuitka-project: --file-description=teRMo
# nuitka-project: --include-data-files={MAIN_DIRECTORY}/icon.png=data/icon.png
# nuitka-project: --macos-app-icon={MAIN_DIRECTORY}/icon.png
# nuitka-project: --macos-app-protected-resource="NSBluetoothAlwaysUsageDescription:b luetooth access"

from termo import start

if __name__ == "__main__":
    start()