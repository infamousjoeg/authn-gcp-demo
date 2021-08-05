import requests
import json
import os

from flask import Flask

conjurApplianceURL = "https://dap.joegarcia.dev"
conjurAccount = "cyberarkdemo"
app = Flask(__name__)

# Returns signed JWT from local Google Metadata service
def google_jwt(audience):
    # Form headers for Google Metadata request
    headers = {
        'Metadata-Flavor': 'Google',
    }
    # Urlify host identity to apply to audience claim
    audience_claim = audience.replace("/", "%2F")
    # Send request and print response
    jwt_response = requests.request(
        'GET',
        'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience={}&format=full'.format(audience_claim),        headers=headers
    )

    return jwt_response.text

# Returns Conjur session token after successful authentication
def conjur_authenticate(url, account, token):
    # Form headers for Conjur authn-gcp authenticate request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'base64',
    }
    # Form body for Conjur authn-gcp authenticate request
    body = "jwt={}".format(token)
    # Send Google-provided JWT to Conjur authn-gcp authenticate endpoint
    conjur_token = requests.request(
        'POST',
        '{}/authn-gcp/{}/authenticate'.format(url, account),
        headers=headers,
        data=body
    )

    return conjur_token.text

# Returns the secret variable from Conjur
def fetch_secret(url, account, conjur_token, secret_variable):
    # Form header for Conjur API secret retrieval
    header = {
        'Authorization': 'Token token="{}"'.format(conjur_token)
    }

    # Urlify secret variable since it's passed as a URL parameter
    urlified_secret_variable = secret_variable.replace("/", "%2F")

    # Retrieve and print gcp/db_password secret variable value
    conjur_variable = requests.request(
        'GET',
        '{}/secrets/{}/variable/{}'.format(url, account, urlified_secret_variable),
        headers=header
    )

    return conjur_variable.text

# The main route for testing
@app.route("/")
def hello_world():
    jwt = google_jwt(
        "/conjur/authn-gcp/host/gcp/function"
    )
    conjur_token = conjur_authenticate(
        conjurApplianceURL,
        conjurAccount,
        jwt
    )
    secret_value = fetch_secret(
        conjurApplianceURL,
        conjurAccount,
        conjur_token,
        "gcp/db_password"
    )

    return "<p><h2>Google-provided JWT:</h2></p><p>{}</p><p><h2>Conjur Session Token:</h2></p> <p>{}</p><p><h2>Secret Variable Value:</h2></p> <p>{}</p>".format(jwt, conjur_token, secret_value)

# The status route for... well... testing, too
@app.route("/status")
def status():
    return "OK"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))