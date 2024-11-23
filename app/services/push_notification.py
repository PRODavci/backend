import os
from base64 import b64decode
import json
from google.oauth2 import service_account
import aiohttp

CREDS = os.getenv("CREDS")

def fix_base64_padding(b64_string):
    missing_padding = len(b64_string) % 4
    if missing_padding:
        b64_string += '=' * (4 - missing_padding)
    return b64_string

SERVICE_ACCOUNT_INFO = b64decode(fix_base64_padding(os.getenv("CREDS"))).decode("utf-8")
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

async def get_access_token_async():
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(SERVICE_ACCOUNT_INFO), scopes=SCOPES
    )

    request_url = 'https://oauth2.googleapis.com/token'
    async with aiohttp.ClientSession() as session:
        async with session.post(
            request_url,
            data={
                'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                'assertion': credentials._make_authorization_grant_assertion()
            }
        ) as response:
            response_data = await response.json()
            return response_data.get('access_token')

async def send_push_notification_async(title, body, devices_tokens):
    token = await get_access_token_async()
    url = 'https://fcm.googleapis.com/v1/projects/mirea-scanner/messages:send'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    payload = {
        'message': {
            'token': devices_tokens,
            'notification': {
                'title': title,
                'body': body,
            },
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            response_data = await response.json()
            print('Request for FCM:', payload)
            print('Response from FCM:', response_data)