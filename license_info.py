from __future__ import unicode_literals
import sys

from pip import get_installed_distributions
from pkgtools.pypi import PyPIXmlRpc
try:
    import termcolor
    USE_TERMCOLOR = True
except ImportError:
    USE_TERMCOLOR = False


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

UNKNOWN_STR = "UNKNOWN"


def format_license(license, ok=True):
    # Avoid sending garbage to the output when being piped.
    if USE_TERMCOLOR and sys.stdout.isatty():
        return termcolor.colored(
            license, ok and "green" or "red", attrs=["bold"])
    return license


def get_license_line(name, version, license):
    ok = license in GOOD_LICENSES

    return ''.join([
        "%s==%s #" % (name, version),
        format_license(license, ok),
    ])


def display(name, version, license, stream=None):
    stream = stream or DEFAULT_STREAM
    line = get_license_line(name, version, license)
    stream.write(line)
    stream.write('\n')


def find_classifier(classifiers):
    for row in classifiers:
        if row.startswith("License"):
            return row


def extract_license(pkg_info):
    # 1st try: raw `license` field.
    license = pkg_info.get("license", UNKNOWN_STR).strip()
    if license != UNKNOWN_STR:
        return license

    # 2nd try: parsing classifiers.
    matched = find_classifier(pkg_info.get("classifiers", []))
    if matched:
        return matched.split("::")[-1].strip()

    return UNKNOWN_STR


def display_dist(dist):
    name, version = dist.project_name, dist.version

    info = api.release_data(name, version)
    license = extract_license(info)

    display(name, version, license)


def main():
    for dist in get_installed_distributions():
        display_dist(dist)


if __name__ == '__main__':
    main()

