import requests
import json
import os

from flask import Flask

app = Flask(__name__)


# The main route for testing
@app.route("/")
def index():
    # Form headers for Google Metadata request
    jwt_headers = {
        'Metadata-Flavor': 'Google',
    }

    # Urlify host identity to apply to audience claim
    audience_claim = "cloud%2Fgcp%2Ffunction%2Fproject2"

    # Send request and print response
    jwt_response = requests.request(
        'GET',
        'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience={}&format=full'.format(audience_claim),
        headers=jwt_headers
    )
    returned_response = "<h2>Google Provided JWT:</h2> <p>{}</p>".format(jwt_response.text)

    # Form headers for Conjur authn-gcp authenticate request
    conjur_token_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'base64',
    }

    # Form body for Conjur authn-gcp authenticate request
    conjur_token_body = "jwt={}".format(jwt_response.text)

    # Send Google Provided JWT to Conjur authn-gcp authenticate endpoint
    conjur_token = requests.request(
        'POST',
        'https://conjur.joegarcia.dev/authn-gcp/cyberarkdemo/authenticate',
        headers=conjur_token_headers,
        data=conjur_token_body
    )
    returned_response += "<h2>Conjur Session Token:</h2> <p>{}</p>".format(conjur_token.text)

    # Form header for Conjur API secret retrieval
    header = {
        'Authorization': 'Token token="{}"'.format(conjur_token.text)
    }

    # Retrieve and print gcp/db_password secret variable value
    conjur_variable = requests.request(
        'GET',
        'https://conjur.joegarcia.dev/secrets/cyberarkdemo/variable/cloud%2Fgcp%2Ffunction%2Fdb_password',
        headers=header
    )
    returned_response += "<h2>Conjur Secret Variable Value:</h2> <p>{}</p>".format(conjur_variable.text)

    return returned_response

# The status route for... well... testing, too
@app.route("/status")
def status():
    return "OK"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))