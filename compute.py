#!/usr/bin/env python3

import requests


def get_id_token(audience):
  token_response = requests.get(f'http://metadata/computeMetadata/v1/instance/service/accounts/default/identity?audience={audience}', headers={'Metadata-Flavor': 'Google'})
  return token_response.text


def conjur_authenticate(url, account, token):
  conjur_token = requests.post(f'{url}/authn-gcp/{account}/authenticate', headers={'Content-Type': 'application/x-www-form-urlencoded', 'Accept-Encoding': 'base64'})


##########
## Main ##
##########

if __name__ == "__main__":
  token = get_id_token("conjur/cyberarkdemo/host/gcp/compute")
  print("Google Provided JWT: %s").format(token)  
  
  #curl -k --request POST \
  #  'https://ec2-0-000-000-00.eu-central-1.compute.amazonaws.com/authn-gcp/myorg/authenticate' --header 'Content-Type: application/x-www-form-urlencoded'\ 
  #  --header "Accept-Encoding: base64" \ 
  #  --data-urlencode 'jwt=eyJ0e......jjjkl'

  # Send JWT to authn-gcp authenticator in Conjur API

  # Receive JWT Conjur session token in return

  # Retrieve secrets

  # Print secrets

