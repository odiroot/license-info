from __future__ import unicode_literals
from pip import get_installed_distributions
from pkgtools.pypi import PyPIXmlRpc
import sys


api = PyPIXmlRpc()

DEFAULT_STREAM = sys.stdout

GOOD_LICENSES = set([
    "Apache Software License",
    "Apache",
    "BSD License",
    "BSD",
    "MIT License",
    "MIT",
    # ...
])


def get_license_line(name, version, license):
    ok = license in GOOD_LICENSES
    return ''.join([
        "%s==%s #" % (name, version),
        (ok and "\033[92m" or "\033[91m") + license + "\033[0m",
    ])

def display(name, version, license, stream=None):
    stream = stream or DEFAULT_STREAM
    line = get_license_line(name, version, license)
    stream.write(line)
    stream.write('\n')


def display_dist(dist):
    name, version = dist.project_name, dist.version

    info = api.release_data(name, version)
    license = info.get("license", "UNKNOWN").strip()

    display(name, version, license)

def main():
    for dist in get_installed_distributions():
        display_dist(dist)


if __name__ == '__main__':
    main()

