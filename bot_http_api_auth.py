import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

# Load Auth 
CLIENT_ID = os.environ['DISCORD_CLIENT_ID']
CLIENT_SECRET = os.environ['DISCORD_SECRET']
BASE_URL = "https://discord.com/api/v10"

def get_token():
  data = {
    'grant_type': 'client_credentials',
    'scope': 'identify connections'
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post(f'{BASE_URL}/oauth2/token', data=data, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET))
  r.raise_for_status()
  logging.info(f"API Authorization - Received HTTP Code: {r.status_code} -> Reason:  {r.reason}")
  r_dict = r.json()
  return r_dict['access_token']

if __name__ == "__main__":
  access_token = get_token()
  headers = {
      'Authorization': f'Bearer {access_token}',
  }
  r = requests.get(f'{BASE_URL}/oauth2/applications/@me',  headers=headers)
  print(f"Received HTTP Code: {r.status_code} -> Reason:  {r.reason}")
  print(r.json())
