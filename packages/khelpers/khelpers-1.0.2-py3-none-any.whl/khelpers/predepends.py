import pip


def installifneeded(packages):
    if isinstance(packages, list):
        package_list = packages
    elif isinstance(packages, str):
        package_list = [packages]
    else:
        TypeError("Packages var must be str or list.")

    for package in package_list:
        try:
            __import__(package)
        except ImportError:
            pip.main(['install', package])
