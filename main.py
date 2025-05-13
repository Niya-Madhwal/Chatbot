from fastapi import FastAPI
import msal, requests, os
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

print("TENANT_ID:", TENANT_ID)

app = FastAPI()


AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
SCOPE = ['https://graph.microsoft.com/.default']

def get_access_token():
    print("🔐 Requesting token...")  # Debug log

    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )

    result = app.acquire_token_for_client(scopes=SCOPE)

    print("🎯 Token result:", result)  # Log full token response

    if "access_token" in result:
        return result['access_token']
    else:
        raise Exception(f"Auth failed: {result.get('error_description')}")


@app.get("/users")
def fetch_users():
    try:
        token = get_access_token()
        headers = {'Authorization': f'Bearer {token}'}

        response = requests.get(
            'https://graph.microsoft.com/v1.0/users',
            headers=headers
        )

        print("🔹 Graph API Status:", response.status_code)
        print("🔹 Graph API Response:", response.text)

        return response.json()
    except Exception as e:
        print("❌ Internal error:", str(e))
        return {
            "error": "Internal Server Error",
            "details": str(e)
        }

@app.get("/devices")
def fetch_devices():
    token = get_access_token()
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('https://graph.microsoft.com/v1.0/deviceManagement/managedDevices', headers=headers)
    return response.json()
