"""Tests for certbot_dns_myonlineportal.dns_myonlineportal."""

import unittest

import mock
import requests
import requests_mock

from certbot import errors
from certbot.compat import os
from certbot.plugins import dns_test_common
from certbot.plugins.dns_test_common import DOMAIN
from certbot.tests import util as test_util

FAKE_USER = "remoteuser"
FAKE_PW = "password"
FAKE_ENDPOINT = "mock://endpoint"


class AuthenticatorTest(
    test_util.TempDirTestCase, dns_test_common.BaseAuthenticatorTest
):
    def setUp(self):
        super(AuthenticatorTest, self).setUp()

        from certbot_dns_myonlineportal.dns_myonlineportal import Authenticator

        path = os.path.join(self.tempdir, "file.ini")
        dns_test_common.write(
            {
                "myonlineportal_username": FAKE_USER,
                "myonlineportal_password": FAKE_PW,
                "myonlineportal_endpoint": FAKE_ENDPOINT,
            },
            path,
        )

        super(AuthenticatorTest, self).setUp()
        self.config = mock.MagicMock(
            myonlineportal_credentials=path, myonlineportal_propagation_seconds=0
        )  # don't wait during tests

        self.auth = Authenticator(self.config, "myonlineportal")

        self.mock_client = mock.MagicMock()
        # _get_myonlineportal_client | pylint: disable=protected-access
        self.auth._get_myonlineportal_client = mock.MagicMock(return_value=self.mock_client)

    # def test_perform(self):
    #     self.auth.perform([self.achall])

    #     expected = [
    #         mock.call.add_txt_record(
    #             DOMAIN, "_acme-challenge." + DOMAIN, mock.ANY, mock.ANY
    #         )
    #     ]
    #     self.assertEqual(expected, self.mock_client.mock_calls)

    def test_cleanup(self):
        # _attempt_cleanup | pylint: disable=protected-access
        self.auth._attempt_cleanup = True
        self.auth.cleanup([self.achall])

        expected = [
            mock.call.del_txt_record(
                DOMAIN, "_acme-challenge." + DOMAIN, mock.ANY, mock.ANY
            )
        ]
        self.assertEqual(expected, self.mock_client.mock_calls)


class MyOnlinePortalClientTest(unittest.TestCase):
    record_name = "foo"
    record_content = "bar"
    record_ttl = 42

    def setUp(self):
        from certbot_dns_myonlineportal.dns_myonlineportal import _MyOnlinePortalClient

        self.adapter = requests_mock.Adapter()

        self.client = _MyOnlinePortalClient(FAKE_ENDPOINT, FAKE_USER, FAKE_PW)
        self.client.session.mount("mock", self.adapter)

    def _register_response(self, code=None, text=None):
        self.adapter.register_uri('GET', FAKE_ENDPOINT, status_code=code, text=text)

    def test_add_txt_record(self):
        self._register_response(200, text="set to ")
        self.client.add_txt_record(
            DOMAIN, self.record_name, self.record_content, self.record_ttl
        )

    def test_add_txt_record_fail_to_find_domain(self):
        self._register_response(code=404, text="nohost - domain not found")
        with self.assertRaises(errors.PluginError):
            self.client.add_txt_record(
                DOMAIN, self.record_name, self.record_content, self.record_ttl
            )

    def test_add_txt_record_fail_to_authenticate(self):
        self._register_response(code=401, text="badauth")
        with self.assertRaises(errors.PluginError):
            self.client.add_txt_record(
                DOMAIN, self.record_name, self.record_content, self.record_ttl
            )

    def test_del_txt_record(self):
        self._register_response(code=200, text="")
        self.client.del_txt_record(
            DOMAIN, self.record_name, self.record_content, self.record_ttl
        )

    def test_del_txt_record_fail_to_find_domain(self):
        self._register_response(code=404, text="nohost - domain not found")
        with self.assertRaises(errors.PluginError):
            self.client.del_txt_record(
                DOMAIN, self.record_name, self.record_content, self.record_ttl
            )


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
