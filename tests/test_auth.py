import uuid
import pytest
import json
from unittest.mock import patch
import responses

from msal import ConfidentialClientApplication
from flask import url_for, session, get_flashed_messages

from tools.auth import AuthHandler
from tools.errors import AuthException
from tools.database.models import User
from tests.conftest import mock_user


def test_unauthed_homepage(app, client):
    """
    Test that the homepage includes a `Click to log in` link
    """
    with app.test_request_context():
        response = client.get("/")
        assert response.status_code == 200
        body = response.data
        assert b"Click to log in" in body


def test_auth_client(app):
    assert isinstance(app.auth, AuthHandler)
    assert isinstance(app.auth.client, ConfidentialClientApplication)

    with app.test_request_context():
        assert app.auth.get_logout_url().endswith(url_for("tools.index"))


@responses.activate
def test_auth_process(app, client, db_session):
    """
    Test the authentication workflow
    """
    responses.add(
        responses.GET,
        "https://graph.microsoft.com/v1.0/me/",
        match_querystring=False,
        json={
            "businessPhones": [],
            "displayName": "Ada Lovelace",
            "givenName": "Ada",
            "jobTitle": None,
            "mail": "alovelace@olin.edu",
            "mobilePhone": None,
            "officeLocation": None,
            "preferredLanguage": None,
            "surname": "Lovelace",
            "userPrincipalName": "alovelace@olin.edu",
            "id": "ac19540c-210b-ff37-asdf-10293abfe9se",
        },
    )

    with app.test_request_context():
        # User not logged in yet, goes to /
        with patch.object(
            AuthHandler, "get_auth_url", return_value="https://example.com"
        ) as mock_method:
            response = client.get("/")
            assert mock_method.called
            assert response.data == b"<a href='https://example.com'>Click to log in</a>"

        # Get a token, mock out the acquire_token thing
        token = uuid.uuid4()
        with patch.object(
            ConfidentialClientApplication,
            "acquire_token_by_authorization_code",
            return_value={
                "access_token": str(token),
                "id_token_claims": {
                    "oid": "ac19540c-210b-ff37-asdf-10293abfe9se",
                    "name": "Ada",
                    "mail": "alovelace@olin.edu",
                },
                "refresh_token": "refresh_token",
            },
        ) as mock_method:
            with client.session_transaction() as sess:
                sess["state"] = "test_state"

            # This would be a request from Microsoft to tools.olin.edu
            with client:
                response = client.get(
                    "/auth/token",
                    query_string={
                        "state": "test_state",
                        "access_token": str(token),
                        "code": "test_code",
                    },
                )
                assert (
                    session["user"].get("oid") == "ac19540c-210b-ff37-asdf-10293abfe9se"
                )

                # Now the homepage displays a custom message
                response = client.get("/")
                assert b"Welcome Ada" in response.data

                # Logout
                response = client.get("/auth/logout")
                assert session.get("user") is None
                assert response.status_code == 302
                # Needs to be `in` in case the AZURE_TENANT_ID isn't set
                assert app.auth.get_logout_url() in response.headers["location"]

            # User should be saved in the database
            assert (
                db_session.query(User).first().user_id
                == "ac19540c-210b-ff37-asdf-10293abfe9se"
            )


def test_auth_failure(app, client):
    with patch.object(
        ConfidentialClientApplication,
        "acquire_token_by_authorization_code",
        return_value={"error": "some error"},
    ):
        with pytest.raises(AuthException):
            app.auth.get_token("mock_code", ["Scope"], "some_url")

        resp = client.get("/auth/token", query_string={"code": "code"})
        assert {
            "message": "Error acquiring token: some error",
            "code": 401,
        } == json.loads(resp.data)

    resp = client.get("/auth/token", query_string={"error": "Could not retrieve token"})
    assert json.loads(resp.data) == {
        "message": "Exception in auth process: Could not retrieve token",
        "code": 500,
    }

    # State failure
    with client.session_transaction() as sess:
        sess["state"] = "state"

    response = client.get("/auth/token", query_string={"state": "wrong_state"})
    assert response.status_code == 400

    with client:
        response = client.get("/auth/token", query_string={"state": "state"})
        assert {"code": 400, "message": "No code provided"} == json.loads(response.data)
        assert "No code provided" in get_flashed_messages()


@responses.activate
def test_get_current_user(app):
    responses.add(
        responses.GET,
        "https://graph.microsoft.com/v1.0/me/",
        match_querystring=False,
        json={
            "businessPhones": [],
            "displayName": "Ada Lovelace",
            "givenName": "Ada",
            "jobTitle": None,
            "mail": "alovelace@olin.edu",
            "mobilePhone": None,
            "officeLocation": None,
            "preferredLanguage": None,
            "surname": "Lovelace",
            "userPrincipalName": "alovelace@olin.edu",
            "id": "ac19540c-210b-ff37-asdf-10293abfe9se",
        },
    )
    with patch.object(AuthHandler, "get_auth_headers", return_value={}):
        current_user = app.auth.get_current_user()

        assert responses.calls[0].request.params == {
            "$select": "id,displayName,mail,givenName,surname"
        }
        assert current_user == {
            "email": "alovelace@olin.edu",
            "display_name": "Ada Lovelace",
            "first_name": "Ada",
            "last_name": "Lovelace",
            "user_id": "ac19540c-210b-ff37-asdf-10293abfe9se",
        }


@responses.activate
def test_existing_user(app, client, db_session):
    """
    User already exists, but they have a new email for some reason
    """
    mock_user(
        1,
        db_session,
        user_id="ac19540c-210b-ff37-asdf-10293abfe9se",
        email="alovelace@olin.edu",
    )
    responses.add(
        responses.GET,
        "https://graph.microsoft.com/v1.0/me/",
        match_querystring=False,
        json={
            "businessPhones": [],
            "displayName": "Ada Lovelace",
            "givenName": "Ada",
            "jobTitle": None,
            "mail": "Ada.Lovelace@olin.edu",
            "mobilePhone": None,
            "officeLocation": None,
            "preferredLanguage": None,
            "surname": "Lovelace",
            "userPrincipalName": "Ada.Lovelace@olin.edu",
            "id": "ac19540c-210b-ff37-asdf-10293abfe9se",
        },
    )

    with app.test_request_context():
        # Get a token, mock out the acquire_token thing
        token = uuid.uuid4()
        with patch.object(
            ConfidentialClientApplication,
            "acquire_token_by_authorization_code",
            return_value={
                "access_token": str(token),
                "id_token_claims": {
                    "oid": "ac19540c-210b-ff37-asdf-10293abfe9se",
                    "name": "Ada",
                    "mail": "Ada.Lovelace@olin.edu",
                },
                "refresh_token": "refresh_token",
            },
        ):
            with client.session_transaction() as sess:
                sess["state"] = "test_state"

            client.get(
                "/auth/token",
                query_string={
                    "state": "test_state",
                    "access_token": str(token),
                    "code": "test_code",
                },
            )

            # User should be updated in the database
            assert db_session.query(User).first().email == "Ada.Lovelace@olin.edu"
