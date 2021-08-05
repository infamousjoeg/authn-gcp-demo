# authn-gcp-demo

This is a demonstration of authn-gcp for [CyberArk Conjur](https://conjur.org).

# How it works?

An application or script hosted in Google Compute Engine (GCE) or a Google Cloud Run function can request a signed JWT from Google's local Metadata service with a provided `audience` claim for a Conjur Host Identity. When this JWT is used to authenticate over Conjur's authn-gcp authenticate endpoint, it is decrypted against Google's service and checked against Conjur policy to match `service-account-id` and `service-account-email`. Those values will match the assigned Service Account to the resource in GCP and can be verified by Conjur's service.  If all checks pass, a Conjur session token is returned to the application or script.

# Usage

## Google Compute Engine

1. Modify the Jinja variables in [policies/gcp.yml](policies/gcp.yml) and load both policies in [policies/](policies/) into the Conjur Leader.
2. Initialize a secret value to the variables just created: `gcp/db_username` and `gcp/db_password`.
3. SSH onto the GCE VM and `git clone` this repository.
   1. If using `gcloud`, `gcloud beta compute ssh --zone "<<availability-zone>>" "<<vm-name>>" --project "<<project-id>>"`
4. `pip` is not installed in GCE VM's by default. You'll need to run `sudo apt install python3-pip -y`.
5. Once `pip` is installed, from within the cloned repo root directory, run `pip3 install -r requirements.txt`.
6. From there, `./compute.py` is executable without prefacing with `python3`.

## Google Cloud Run

1. Follow steps #1 and #2 from the [Google Compute Engine](#google-compute-engine) section if they were not previously done.
2. Log into the Google Cloud Console and navigate to the Cloud Run service portal.
3. Click "Create Service" to create your service.
   1. By default, the Compute default service account will be applied. If you change it, you will need to ensure that the `service-account-id` and `service-account-email` values for the function host identity in Conjur reflects the proper values.
4. Once the service is created, you can use Google Cloud CLI `gcloud` to build and run the Python-based service container in this project.
5. `gcloud builds submit --tag gcr.io/<<project-id>>/<<gcr-service-name>>`
6. `gcloud run deploy --image gcr.io/<<project-id>>/<<gcr-service-name>>`
7. Once the container is deployed and available as a service, a URL will be reported to STDOUT.

# Expected Results

If successful, your Google-provided JWT, Conjur session token, and secret set to `gcp/db_password` will be echo'ed to STDOUT. If browsing to the Google Cloud Run service webpage, they will be displayed on the index page.

# Troubleshooting

### Google Provided JWT Returned, No Conjur Session Token

Make sure that your `audience` claim value in the Python scripts are "urlified":

__GOOD__
`audience_claim = "conjur%2Fauthn-gcp%2Fhost%2Fgcp%2Fcompute"`

__BAD__
`audience_claim = "conjur/authn-gcp/host/gcp/compute"`

If your `audience` claim is "urlified", check the `email` and `sub` claims of the encoded JWT token:

1. You need to decode the JWT token to read the claims. To do this, browse to [jwt.io](https://jwt.io).
2. Scroll down to the "Debugger" section and select `RS256` for the Algorithm from the drop-down selector.
3. Copy and paste your Google-provided encoded JWT into the "Encoded" section.
4. On the right-hand side under "Decoded," in the "Payload" section, verify the `email` matches that of your assigned service account in GCP IAM. Also, verify that the `sub` value matches the service account's ID in GCP IAM.

# License

MIT