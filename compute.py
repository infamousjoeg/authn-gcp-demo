#!/usr/bin/env python3

import requests
import json

# Form headers for Google Metadata request
jwt_headers = {
    'Metadata-Flavor': 'Google',
}

# Urlify host identity to apply to audience claim
audience_claim = "conjur%2Fcyberarkdemo%2Fhost%2Fgcp%2Fcompute"

# Send request and print response
jwt_response = requests.request('GET', 'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience={}'.format(audience_claim), headers=jwt_headers)
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
print("Conjur Session Token: {}".format(conjur_token.text))

  #curl -k --request POST \
  #  'https://ec2-0-000-000-00.eu-central-1.compute.amazonaws.com/authn-gcp/myorg/authenticate' --header 'Content-Type: application/x-www-form-urlencoded'\ 
  #  --header "Accept-Encoding: base64" \ 
  #  --data-urlencode 'jwt=eyJ0e......jjjkl'

  # Send JWT to authn-gcp authenticator in Conjur API

  # Receive JWT Conjur session token in return

  # Retrieve secrets

  # Print secrets

