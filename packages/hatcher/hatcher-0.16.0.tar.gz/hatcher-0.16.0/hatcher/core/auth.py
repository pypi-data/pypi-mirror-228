#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
import time
from threading import RLock

import requests
from requests.auth import AuthBase

# Renew the session token this frequently (seconds)
REAUTH_INTERVAL = 4 * 60

# Prevent multiple threads from fighting over the renewal
LOCK = RLock()


class BroodClientAuth(AuthBase):
    def __init__(self, brood_url, credentials, verify_ssl=None):
        """ Create an auth object backed by an offline token or username
        and password.

        Parameters
        ----------
        brood_url : str
            URL for the brood server, e.g. "https://packages.enthought.com".
        credentials : str, tuple(str, str)
            Offline token; what would go in .edm.yaml or $HATCHER_TOKEN. Can
            also be a tuple of (username, password).
        verify_ssl : Bool
            Whether to use SSL verification when communicating with Brood to
            issue a session token.  Default is to verify.
        """

        if verify_ssl is None:
            self.verify_ssl = True
        else:
            self.verify_ssl = verify_ssl

        # I don't know how much validation is needed here, but these seem like
        # possible common mistakes. Note: we can't raise any exceptions in the
        # constructor, since the auth object is created very early on in the
        # Click startup process and --help still needs to work.
        if brood_url.endswith('/'):
            brood_url = brood_url[0:-1]
        if not brood_url.startswith('http'):
            brood_url = 'https://' + brood_url

        self.brood_url = brood_url

        self.credentials = credentials

        self.session_token = None
        self._last_refresh = time.time() - (REAUTH_INTERVAL * 2)

    def _refresh(self):
        """ Obtain a new session token, if needed. """

        with LOCK:

            # Unfortunately we do not have time.monotonic() on 2.7,
            # so try to catch clock changes resulting in a negative delta.
            delta = time.time() - self._last_refresh
            if 0 <= delta <= REAUTH_INTERVAL:
                return

            self.session_token = self._get_token()
            self._last_refresh = time.time()

    def _get_token(self):
        """ Fetch a new session token. """
        url = '{}/api/v1/json/auth/tokens/auth'.format(self.brood_url)

        if isinstance(self.credentials, tuple):
            # If username/password, use a different auth style.
            result = requests.post(
                url,
                auth=self.credentials,
                data={},
                verify=self.verify_ssl
            )
        else:
            result = requests.post(
                url,
                headers={'Authorization': 'Bearer {}'.format(self.credentials)
                         },
                data={},
                verify=self.verify_ssl
            )
        if not result.ok:
            result.raise_for_status()

        return result.json()['token']

    def __call__(self, request):
        self._refresh()
        request.headers['Authorization'] = 'Bearer {0}'.format(
            self.session_token)
        return request
