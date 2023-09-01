from pathlib import Path
from loguru import logger

import os

def check_subpackages_for_plugin(root_package: Path | str):
    subpackage_names = []
    for root, _, files in os.walk(root_package):
        if "__init__.py" in files:
            package_name = os.path.basename(root)
            subpackage_names.append(package_name)

    plugin_subpackages = []
    for subpackage_name in subpackage_names:
        subpackage_module = subpackage_name #f"{str(root_package).split('.')[-1]}.{subpackage_name}"
        print(subpackage_module)
        try:
            subpackage = __import__(subpackage_module, fromlist=['__type__'])
            if hasattr(subpackage, '__type__'):
                if subpackage.__type__ == "plugin":
                    plugin_subpackages.append(subpackage_name)
        except ImportError as error:
            logger.exception(error)

    return plugin_subpackages

if __name__ == "__main__":
    root_package = Path(__file__).resolve().parent  # Replace with your root package name
    plugin_subpackages = check_subpackages_for_plugin(root_package)
    print("Plugin subpackages:", plugin_subpackages)
