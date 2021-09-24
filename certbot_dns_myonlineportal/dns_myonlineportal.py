"""DNS Authenticator for MyOnlinePortal."""
import json
import logging
import time

import requests
import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for MyOnlinePortal
    This Authenticator uses the MyOnlinePortal Remote REST API to fulfill a dns-01 challenge.
    """

    description = "Obtain certificates using a DNS TXT record (if you are using MyOnlinePortal for DNS)."
    ttl = 60

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds=120
        )
        add("credentials", help="MyOnlinePortal credentials INI file.")

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        logger.debug(" _more_info")
        return (
            "This plugin configures a DNS TXT record to respond to a dns-01 challenge using "
            + "the MyOnlinePortal Remote REST API."
        )

    def _setup_credentials(self):
        logger.debug(" _setup_credentials")
        self.credentials = self._configure_credentials(
            "credentials",
            "MyOnlinePortal credentials INI file",
            {
                "endpoint": "URL of the MyOnlinePortal Remote API.",
                "username": "Username for MyOnlinePortal Remote API.",
                "password": "Password for MyOnlinePortal Remote API.",
            },
        )

    def _perform(self, domain, validation_name, validation):
        logger.debug(" _perform")
        self._get_myonlineportal_client().add_txt_record(
            domain, validation_name, validation, self.ttl
        )

    def _cleanup(self, domain, validation_name, validation):
        logger.debug(" _cleanup")
        self._get_myonlineportal_client().del_txt_record(
            domain, validation_name, validation, self.ttl
        )

    def _get_myonlineportal_client(self):
        logger.debug(" _get_myonlineportal_client")
        return _MyOnlinePortalClient(
            self.credentials.conf("endpoint"),
            self.credentials.conf("username"),
            self.credentials.conf("password"),
        )


class _MyOnlinePortalClient(object):
    """
    Encapsulates all communication with the MyOnlinePortal Remote REST API.
    """

    def __init__(self, endpoint, username, password):
        logger.debug("creating myonlineportalclient")
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session_id = None

    def add_txt_record(self, domain, record_name, record_content, record_ttl):
        """
        Add a TXT record using the supplied information.
        :param str domain: The domain to use to look up the managed zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :param int record_ttl: The record TTL (number of seconds that the record may be cached).
        :raises certbot.errors.PluginError: if an error occurs communicating with the MyOnlinePortal API
        """
        logger.debug(
            f"add_txt_record(self, domain={domain}, record_name={record_name}, record_content={record_content}, record_ttl={record_ttl})"
        )
        payload = {'hostname': domain, 'txt': record_content}
        r = self.session.get(self.endpoint, auth=(self.username, self.password), params=payload)
        logger.debug(f"response {r.status_code} = {r.text} ")
        if r.status_code != 200:
            raise errors.PluginError(r.text)

    def del_txt_record(self, domain, record_name, record_content, record_ttl):
        """
        Delete a TXT record using the supplied information.
        :param str domain: The domain to use to look up the managed zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :param int record_ttl: The record TTL (number of seconds that the record may be cached).
        :raises certbot.errors.PluginError: if an error occurs communicating with the MyOnlinePortal API
        """
        logger.debug(
            f"del_txt_record(self, domain={domain}, record_name={record_name}, record_content={record_content}, record_ttl={record_ttl})"
        )
        payload = {'hostname': domain, 'txt': ""}
        r = self.session.get(self.endpoint, auth=(self.username, self.password), params=payload)
        logger.debug(f"response {r.status_code} = {r.text} ")
        if r.status_code != 200:
            raise errors.PluginError(r.text)
