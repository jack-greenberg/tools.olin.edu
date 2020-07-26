import uuid
import logging
import requests

from msal import ConfidentialClientApplication
from flask import session, url_for

from tools.errors import AuthException

from tools.config import AZURE_APPLICATION_ID, AZURE_CLIENT_SECRET, AZURE_AUTHORITY


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AuthHandler(object):
    """
    A wrapper for AzureAD authentication using msal
    """

    @property
    def client(self):
        if not hasattr(self, "azure_client"):
            self.azure_client = ConfidentialClientApplication(
                client_id=AZURE_APPLICATION_ID,
                authority=AZURE_AUTHORITY,
                client_credential=AZURE_CLIENT_SECRET,
            )
        return self.azure_client

    def get_auth_url(self, scopes=None, state=None):
        return self.client.get_authorization_request_url(
            scopes or ["User.ReadBasic.All"],
            state=state or str(uuid.uuid4()),
            redirect_uri="http://localhost:8000/api/token",
            # url_for("tools.index", _external=True)
        )

    def get_token(self, code, scopes, redirect_uri):
        response = self.client.acquire_token_by_authorization_code(
            code, scopes=scopes, redirect_uri=redirect_uri
        )
        if "error" in response:
            raise AuthException("Error acquiring token: %s" % response.get("error"))
        return response

    def get_logout_url(self):
        return (
            AZURE_AUTHORITY
            + "/oauth2/v2.0/logout?post_logout_redirect_uri=http://localhost:8000"
            + url_for("tools.index")
        )

    def get_current_user(self):
        selection = ["id", "displayName", "mail", "givenName", "surname"]
        response = requests.get(
            "https://graph.microsoft.com/v1.0/me/",
            params={"$select": ",".join(selection)},
            headers=self.get_auth_headers(),
        ).json()
        return response

    @staticmethod
    def get_auth_headers():
        return {"Authorization": "Bearer " + session["access_token"]}


def authed(f):
    def wrapped(*args, **kwargs):
        if not session.get("user"):
            raise AuthException("User not logged in")
        return f(*args, **kwargs)

    return wrapped
