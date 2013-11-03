from __future__ import unicode_literals
import license_info
import unittest
import io
import mock


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
    def test_main(self, get_installed_distributions, display, api):
        dist1 = mock.Mock()
        dist1.project_name = 'foo'
        dist1.version = '0.9.2'

        dist2 = mock.Mock()
        dist2.project_name = 'bar'
        dist2.version = '2.1.9b'

        get_installed_distributions.return_value = [dist1, dist2]

        api.release_data.return_value = {'license': ' GPL 2  '}

        license_info.main()

        self.assertEqual(display.call_args_list, [
            mock.call('foo', '0.9.2', 'GPL 2'),
            mock.call('bar', '2.1.9b', 'GPL 2'),
        ])


if __name__ == '__main__':
    unittest.main()

