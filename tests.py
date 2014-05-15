from __future__ import unicode_literals
import license_info
import unittest
import io
import mock
import os.path


class TestLicenseInfo(unittest.TestCase):
    @mock.patch("license_info.USE_TERMCOLOR", False)
    @mock.patch("sys.stdout")
    def test_format_license_raw(self, stdout):
        good = license_info.format_license("qux", True)
        self.assertEqual(good, "qux")

        bad = license_info.format_license("ham", False)
        self.assertEqual(bad, "ham")

    @mock.patch("license_info.USE_TERMCOLOR", True)
    @mock.patch("sys.stdout")
    def test_format_license_piped(self, stdout):
        stdout.isatty.return_value = False

        good = license_info.format_license("foo", True)
        self.assertEqual(good, "foo")

        bad = license_info.format_license("bar", False)
        self.assertEqual(bad, "bar")

    @mock.patch("sys.stdout")
    def test_format_license_color(self, stdout):
        stdout.isatty.return_value = True

        good = license_info.format_license("foo", True)
        self.assertEqual(good, "\033[1m\033[32mfoo\033[0m")

        bad = license_info.format_license("bar", False)
        self.assertEqual(bad, "\033[1m\033[31mbar\033[0m")

    @mock.patch("license_info.format_license", lambda a, b: a)
    def test_get_license_line(self):
        line = license_info.get_license_line('foobar', '0.9.0', 'MIT')
        self.assertEqual(line, 'foobar==0.9.0 #MIT')

    @mock.patch("license_info.format_license", lambda a, b: a)
    def test_display(self):
        stream = io.StringIO()
        license_info.display('foobar', '0.9.0', 'MIT', stream=stream)
        self.assertEqual(stream.getvalue(), 'foobar==0.9.0 #MIT\n')

    @mock.patch('license_info.api')
    @mock.patch('license_info.display')
    def test_display_dist_unknown_license(self, display, api):
        dist = mock.Mock()
        dist.project_name = 'foobar'
        dist.version = '1.0'

        api.release_data.return_value = {'platform': 'linux'}
        license_info.display_dist(dist)
        display.assert_called_once_with('foobar', '1.0', 'UNKNOWN')

    @mock.patch('license_info.api')
    @mock.patch('license_info.display')
    @mock.patch('license_info.get_installed_distributions')
    @mock.patch('license_info.read_cache')
    @mock.patch('license_info.write_cache')
    def test_main(self, write_cache, read_cache, get_installed_distributions, display, api):
        dist1 = mock.Mock()
        dist1.project_name = 'foo'
        dist1.version = '0.9.2'

        dist2 = mock.Mock()
        dist2.project_name = 'bar'
        dist2.version = '2.1.9b'

        get_installed_distributions.return_value = [dist1, dist2]

        api.release_data.return_value = {'license': ' GPL 2  '}

        read_cache.return_value = {}

        license_info.main()

        self.assertEqual(display.call_args_list, [
            mock.call('foo', '0.9.2', 'GPL 2'),
            mock.call('bar', '2.1.9b', 'GPL 2'),
        ])

        write_cache.assert_called_once_with({
            ("foo", "0.9.2"): "GPL 2",
            ("bar", "2.1.9b"): "GPL 2",
        })

    def test_extract_license_unknown(self):
        empty_case = {}
        result = license_info.extract_license(empty_case)
        self.assertEqual(result, "UNKNOWN")

        missing_case = {"name": "some-package", "version": "1.0"}
        result = license_info.extract_license(missing_case)
        self.assertEqual(result, "UNKNOWN")

        none_case = {"license": None}
        result = license_info.extract_license(none_case)
        self.assertEqual(result, "UNKNOWN")

    def test_extract_license_usual(self):
        info = {"license": "FOOBAR"}
        result = license_info.extract_license(info)
        self.assertEqual(result, "FOOBAR")

    def test_find_classifier(self):
        empty_case = []
        result = license_info.find_classifier(empty_case)
        self.assertEqual(result, None)

        exists_case = ["License :: Ham"]
        result = license_info.find_classifier(exists_case)
        self.assertEqual(result, "License :: Ham")

    def test_extract_license_classifiers(self):
        info = {"classifiers": [
            "Topic :: Utilities",
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python",
        ]}
        result = license_info.extract_license(info)
        self.assertEqual(result, "BSD License")

    @mock.patch("license_info.api.release_data")
    def test_fetch_package_info_simple(self, release_data):
        release_data.return_value = {"name": "foo"}
        result = license_info.fetch_package_info("foo", "0.1")
        self.assertEqual(result, {"name": "foo"})

    @mock.patch("license_info.api")
    def test_fetch_package_info_newest(self, api):
        def __release_data(name, version):
            if version == "0.1":
                return {}

            if version == "0.3":
                return {"name": "qux"}

        api.release_data.side_effect = __release_data
        api.package_releases.return_value = ["0.3", "0.2"]

        result = license_info.fetch_package_info("qux", "0.1")
        self.assertEqual(result, {"name": "qux"})

    @mock.patch("license_info.api")
    def test_fetch_package_info_missing(self, api):
        api.release_data.return_value = {}
        api.package_releases.return_value = []

        result = license_info.fetch_package_info("ham", "0.1")
        self.assertEqual(result, {})

    @mock.patch("license_info.USE_APPDIRS", False)
    def test_cache_no_appdirs(self):
        path = license_info.get_cache_path()
        self.assertEqual(os.path.basename(path), "li.db")

    @mock.patch("license_info.USE_APPDIRS", True)
    def test_cache_with_appdirs(self):
        path = license_info.get_cache_path()
        self.assertEqual(os.path.basename(path), "li.db")

    def test_packing_unpacking(self):
        data = {
            (u"foo", "1.2.3"): "GPL",
            ("Bar", u"0.1"): "MIT",
            ("qux-ham", "5"): u"BSD", 
        }

        result = license_info.unpack_cache(license_info.pack_cache(data))
        self.assertEqual(set(result), set(data))


if __name__ == '__main__':
    unittest.main()

