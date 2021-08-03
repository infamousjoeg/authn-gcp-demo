#!/usr/bin/env python3

import requests


def urlify(input_str):
    return input_str.replace('/', '%2F')


def get_id_token(audience):
  header = {
    'Metadata-Flavor': 'Google'
  }

  token_response = requests.get('http://metadata/computeMetadata/v1/instance/service/accounts/default/identity?audience={}'.format(audience), headers=header)
  return token_response.text


def conjur_authenticate(url, account, token):
  header = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'base64'
  }

  conjur_token = requests.post(f'{url}/authn-gcp/{account}/authenticate', headers=header)
  return conjur_token.text


##########
## Main ##
##########

if __name__ == "__main__":
  token = get_id_token(urlify("conjur/cyberarkdemo/host/gcp/compute"))
  print("Google Provided JWT: {}".format(token))
  
  #curl -k --request POST \
  #  'https://ec2-0-000-000-00.eu-central-1.compute.amazonaws.com/authn-gcp/myorg/authenticate' --header 'Content-Type: application/x-www-form-urlencoded'\ 
  #  --header "Accept-Encoding: base64" \ 
  #  --data-urlencode 'jwt=eyJ0e......jjjkl'

  # Send JWT to authn-gcp authenticator in Conjur API

  # Receive JWT Conjur session token in return

  # Retrieve secrets

  # Print secrets

