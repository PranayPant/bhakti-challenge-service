import os
from fastapi import HTTPException
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# The path to your service account key file
# It's highly recommended to store this in an environment variable
KEY_FILE_PATH = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

# Define the scopes for the token.
# This is the scope required to interact with Google Cloud services.
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']


async def get_access_token():
    """Asynchronously generates a Google Cloud access token using a service account."""
    if not KEY_FILE_PATH:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    try:
        # Create credentials from the service account key file
        credentials = service_account.Credentials.from_service_account_file(
            KEY_FILE_PATH,
            scopes=SCOPES
        )

        # The 'refresh' method handles the token generation and expiry
        request = Request()
        credentials.refresh(request)

        return credentials.token
    except Exception as e:
        # Log the error for debugging on the server
        print(f"Error generating access token: {e}")
        raise HTTPException(
            status_code=500,
            detail="Could not generate access token. Please check server logs."
        )
