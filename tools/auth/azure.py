import uuid
import logging
import requests

from msal import ConfidentialClientApplication
from flask import session

from tools.errors import AppException

from tools.config import (
    AZURE_APPLICATION_ID,
    AZURE_TENANT_ID,
    AZURE_CLIENT_SECRET,
    AZURE_AUTHORITY,
)


class AuthException(AppException):
    pass


logger = logging.getLogger("auth")

if not all(
    [AZURE_APPLICATION_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET, AZURE_AUTHORITY]
):
    logger.warning("Running without Azure")


class AuthHandler(object):
    """
    A wrapper for AzureAD authentication using msal
    """

    def __init__(
        self,
        application_id=AZURE_APPLICATION_ID,
        tenant_id=AZURE_TENANT_ID,
        client_secret=AZURE_CLIENT_SECRET,
        authority=AZURE_AUTHORITY,
    ):
        self.application_id = application_id
        self.tenant_id = tenant_id
        self.client_secret = client_secret
        self.authority = authority

    @property
    def client(self):
        if not hasattr(self, "azure_client"):
            self.azure_client = ConfidentialClientApplication(
                AZURE_APPLICATION_ID,
                authority=AZURE_AUTHORITY,
                client_credential=AZURE_CLIENT_SECRET,
            )
        return self.azure_client

    def get_auth_url(self, scopes=None, state=None):
        return self.client.get_authorization_request_url(
            scopes or ["User.ReadBasic.All"],
            state=state or str(uuid.uuid4()),
            # redirect_uri=url_for("tools.index", _external=True)
            redirect_uri="http://localhost:8000/api/token",
        )

    def get_current_user(self, id):
        selection = ["id", "displayName", "mail", "givenName", "surname"]
        endpoint = "https://graph.microsoft.com/v1.0/me/{0}".format(id)

        response = requests.get(
            endpoint, params={"$select": ",".join(selection)}
        ).json()

        return response

    def get_token(self, code, scopes, redirect_uri):
        response = self.client.acquire_token_by_authorization_code(
            code, scopes=scopes, redirect_uri=redirect_uri
        )
        return response


def authed(f):
    def wrapped(*args, **kwargs):
        if not session.get("user"):
            raise AuthException("User not logged in", code=401)
        return f(*args, **kwargs)

    return wrapped
