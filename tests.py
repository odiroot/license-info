from __future__ import unicode_literals
import license_info
import unittest
import io
import mock


class TestLicenseInfo(unittest.TestCase):

    def test_get_license_line(self):
        line = license_info.get_license_line('foobar', '0.9.0', 'MIT')
        self.assertEqual(line, 'foobar==0.9.0 #\033[92mMIT\033[0m')

    def test_get_license_line_bad_license(self):
        line = license_info.get_license_line('foobar', '0.9.0', 'GPL')
        self.assertEqual(line, 'foobar==0.9.0 #\033[91mGPL\033[0m')

    def test_display(self):
        stream = io.StringIO()
        license_info.display('foobar', '0.9.0', 'MIT', stream=stream)
        self.assertEqual(stream.getvalue(), 'foobar==0.9.0 #\033[92mMIT\033[0m')

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

