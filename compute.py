#!/usr/bin/env python3

import requests

# Form headers for Google Metadata request
headers = {
    'Metadata-Flavor': 'Google',
}

# Urlify host identity to apply to audience claim
audience_claim = "conjur%2Fcyberarkdemo%2Fhost%2Fgcp%2Fcompute"

# Send request and print response
response = requests.get('http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience={}'.format(audience_claim), headers=headers)
print("Google Provided JWT: {}".format(response.text))



  #curl -k --request POST \
  #  'https://ec2-0-000-000-00.eu-central-1.compute.amazonaws.com/authn-gcp/myorg/authenticate' --header 'Content-Type: application/x-www-form-urlencoded'\ 
  #  --header "Accept-Encoding: base64" \ 
  #  --data-urlencode 'jwt=eyJ0e......jjjkl'

  # Send JWT to authn-gcp authenticator in Conjur API

  # Receive JWT Conjur session token in return

  # Retrieve secrets

  # Print secrets

