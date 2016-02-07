from __future__ import unicode_literals

import unittest
from contextlib import contextmanager

import mock

import cloudping


class AWSContext(object):
    """Mock for the execution context."""

    function_name = 'CloudPing'
    function_version = '1.0'
    invoked_function_arn = ''
    memory_limit_in_mb = 128
    aws_request_id = '1234567890'
    log_group_name = 'CloudPing'
    log_stream_name = 'CloudPingStream'
    identity = None
    client_context = None

    def get_remaining_time_in_millis(self):
        return 10000


class PingHandlerTestCase(unittest.TestCase):
    """Lambda function to ping requested webpage."""

    @contextmanager
    def assert_remote_call(self, *args, **kwargs):
        """Custom assert for remote requests calls."""
        with mock.patch('cloudping.requests') as mock_requests:
            yield
            mock_requests.request.assert_called_with(*args, **kwargs)
            mock_requests.request.return_value.raise_for_status.assert_called_with()

    def test_ping_default(self):
        """Default settings to ping a site."""
        with self.assert_remote_call(
                'GET', 'http://example.com/', allow_redirects=False, timeout=5):
            cloudping.ping({}, AWSContext())

    def test_domain_option(self):
        """Configure the domain to check."""
        with self.assert_remote_call(
                'GET', 'http://test.example.com/', allow_redirects=False, timeout=5):
            cloudping.ping({'domain': 'test.example.com'}, AWSContext())

    def test_path_option(self):
        """Configure the path to check."""
        with self.assert_remote_call(
                'GET', 'http://example.com/test/', allow_redirects=False, timeout=5):
            cloudping.ping({'path': '/test/'}, AWSContext())

    def test_protocol_option(self):
        """Configure the protocol to check."""
        with self.assert_remote_call(
                'GET', 'https://example.com/', allow_redirects=False, timeout=5):
            cloudping.ping({'protocol': 'https'}, AWSContext())

    def test_method_option(self):
        """Configure the HTTP method to check."""
        with self.assert_remote_call(
                'POST', 'http://example.com/', allow_redirects=False, timeout=5):
            cloudping.ping({'method': 'POST'}, AWSContext())

    def test_redirect_option(self):
        """Configure if redirects are followed for the check."""
        with self.assert_remote_call(
                'GET', 'http://example.com/', allow_redirects=True, timeout=5):
            cloudping.ping({'allow_redirects': True}, AWSContext())

    def test_timeout_option(self):
        """Configure timeout for the check."""
        with self.assert_remote_call(
                'GET', 'http://example.com/', allow_redirects=False, timeout=10):
            cloudping.ping({'timeout': 10}, AWSContext())


if __name__ == '__main__':
    unittest.main()
