from pip import get_installed_distributions
from pkgtools.pypi import PyPIXmlRpc


api = PyPIXmlRpc()

GOOD_LICENSES = set([
    "Apache Software License",
    "Apache",
    "BSD License",
    "BSD",
    "MIT License",
    "MIT",
    # ...
])


def display(name, version, license):
    ok = license in GOOD_LICENSES

    print "%s==%s #" % (name, version),
    print (ok and "\033[92m" or "\033[91m") + license + "\033[0m"


def main():
    for dist in get_installed_distributions():
        name, version = dist.project_name, dist.version

        info = api.release_data(name, version)
        license = info.get("license", "UNKNOWN").strip()

        display(name, version, license)


if __name__ == '__main__':
    main()
