import os

from flask import Flask, redirect, render_template, url_for
from flask_dance.contrib.google import google, make_google_blueprint
from oauthlib.oauth2.rfc6749.errors import (
    InvalidClientIdError,
    TokenExpiredError,
)

from contact_parsing import build_domains

app = Flask(__name__)

# app configuration
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.getenv(
    "GOOGLE_OAUTH_CLIENT_SECRET"
)

# blueprint used for auth by flask_dance
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
    """Main route of the app used to display contact information.

    Returns:
        Text: html template
    """
    if not google.authorized:
        return redirect(url_for("google.login"))

    try:
        resp = google.get(
            "https://people.googleapis.com/v1/people/me/connections?personFields=names,emailAddresses,organizations"
        )
    except (InvalidClientIdError, TokenExpiredError):
        return redirect(url_for("google.login"))

    contacts = resp.json()

    data = build_domains(contacts)

    return render_template("index.html", data=data)
