# authn-gcp-demo

This is a demonstration of authn-gcp for [CyberArk Conjur]().

# How it works?

An application or script hosted in Google Compute Engine (GCE) or a Google Cloud Run function can request a signed JWT from Google's local Metadata service with a provided `audience` claim for a Conjur Host Identity. When this JWT is used to authenticate over Conjur's authn-gcp authenticate endpoint, it is decrypted against Google's service and checked against Conjur policy to match `service-account-id` and `service-account-email`. Those values will match the assigned Service Account to the resource in GCP and can be verified by Conjur's service.  If all checks pass, a Conjur session token is returned to the application or script.

# Usage

1. Modify the Jinja variables in [policies/gcp.yml](policies/gcp.yml) and load both policies in [policies/](policies/) into the Conjur Leader.
2. Initialize a secret value to the variables just created: `gcp/db_username` and `gcp/db_password`.
3. SSH onto the GCE VM and `git clone` this repository.
4. `pip` is not installed in GCE VM's by default. You'll need to run `sudo apt install python3-pip -y`.
5. Once `pip` is installed, from within the cloned repo root directory, run `pip3 install -r requirements.txt`.
6. From there, `./compute.py` is executable without prefacing with `python3`.

# Expected Results

If successful, your Google-provided JWT, Conjur session token, and secret set to `gcp/db_password` will be echo'ed to STDOUT.