import os

from flask import Flask, redirect, url_for
from flask_dance.contrib.google import google, make_google_blueprint
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError

from contact_parsing import build_domains


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY")
    app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.getenv(
        "GOOGLE_OAUTH_CLIENT_SECRET"
    )

    google_blueprint = make_google_blueprint(
        scope=[
            "profile",
            "email",
            "https://www.googleapis.com/auth/contacts.readonly",
        ]
    )

    app.register_blueprint(google_blueprint, url_prefix="/login")

    @app.route("/")
    def index():
        if not google.authorized:
            return redirect(url_for("google.login"))

        resp = google.get(
            "https://people.googleapis.com/v1/people/me/connections?personFields=names,emailAddresses,organizations"
        )
        try:
            assert resp.ok, resp.text
        except TokenExpiredError:
            return redirect(url_for("google.login"))
        contacts = resp.json()

        data = build_domains(contacts)
        return data

    return app


def main():
    app = create_app()

    return app
