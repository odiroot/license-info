from __future__ import unicode_literals
from os import makedirs
from os.path import join, isdir, dirname
import sys
import shelve
import tempfile

from pip import get_installed_distributions
from pkgtools.pypi import PyPIXmlRpc
try:
    import termcolor
    USE_TERMCOLOR = True
except ImportError:
    USE_TERMCOLOR = False
try:
    import appdirs
    USE_APPDIRS = True
except ImportError:
    USE_APPDIRS = False

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
    license = (pkg_info.get("license") or UNKNOWN_STR).strip()
    if license != UNKNOWN_STR:
        return license

    # 2nd try: parsing classifiers.
    matched = find_classifier(pkg_info.get("classifiers", []))
    if matched:
        return matched.split("::")[-1].strip()

    return UNKNOWN_STR


def fetch_package_info(name, version):
    # 1st try: given name, version pair.
    info = api.release_data(name, version)
    if info:
        return info

    # 2nd try: newest version.
    versions = api.package_releases(name)
    if versions:
        return api.release_data(name, versions[0])

    # Simulate unknown package.
    return {}


def display_dist(dist):
    name, version = dist.project_name, dist.version

    info = fetch_package_info(name, version)
    license = extract_license(info)

    display(name, version, license)


def get_cache_path():
    if USE_APPDIRS:
        cache_dir = appdirs.user_cache_dir("license-info", "MO")
    else:
        cache_dir = tempfile.gettempdir()
    return str(join(cache_dir, "li.db"))


def open_cache_db():
    cache_path = get_cache_path()
    cache_dir = dirname(cache_path)

    if not isdir(cache_dir):
        makedirs(cache_dir)

    return shelve.open(cache_path)


def pack_cache(data):
    return dict(
        (str(" ".join(k)), v) for k, v in data.items()
    )


def unpack_cache(data):
    return dict(
        (tuple(k.split()), v) for k, v in data.items()
    )


def write_cache(data):
    cache = open_cache_db()
    cache.update(pack_cache(data))
    cache.close()


def read_cache():
    cache = open_cache_db()
    data = dict(cache)
    cache.close()
    return unpack_cache(data)


def main():
    for dist in get_installed_distributions():
        display_dist(dist)


if __name__ == '__main__':
    main()

