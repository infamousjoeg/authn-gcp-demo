#!/usr/bin/env python3

import requests
import json

# Form headers for Google Metadata request
jwt_headers = {
    'Metadata-Flavor': 'Google',
}

# Urlify host identity to apply to audience claim
audience_claim = "conjur%2Fcyberarkdemo%2Fhost%2Fgcp%2Ffunction"

# Send request and print response
jwt_response = requests.request('GET', 'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience={}&format=full'.format(audience_claim), headers=jwt_headers)
print("Google Provided JWT: {}".format(jwt_response.text))

# Form headers for Conjur authn-gcp authenticate request
conjur_token_headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'base64',
}

# Form body for Conjur authn-gcp authenticate request
conjur_token_body = "jwt={}".format(jwt_response.text)

# Send Google Provided JWT to Conjur authn-gcp authenticate endpoint
conjur_token = requests.request('POST', 'https://dap.joegarcia.dev/authn-gcp/cyberarkdemo/authenticate', headers=conjur_token_headers, data=conjur_token_body)
print()
print("Conjur Session Token: {}".format(conjur_token.text))

# Form header for Conjur API secret retrieval
header = {
    'Authorization': 'Token token="{}"'.format(conjur_token.text)
}

# Retrieve and print gcp/db_password secret variable value
conjur_variable = requests.request(
    'GET',
    'https://dap.joegarcia.dev/secrets/cyberarkdemo/variable/gcp%2Fdb_password',
    headers=header
)
print()
print("Conjur Secret Variable Value: {}".format(conjur_variable.text))