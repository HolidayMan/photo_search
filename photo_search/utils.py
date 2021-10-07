from typing import List, Dict
import os.path

import requests
from django.conf import settings


def search_for_images(query: str) -> dict:
    url = f'https://api.shutterstock.com/v2/images/search'
    headers = {'Authorization': f'Bearer {settings.SHUTTERSTOCK_API_TOKEN}'}
    urlparams = {'query': query, 'per_page': 20}
    response = requests.get(url, headers=headers, params=urlparams)
    return response.json()


def build_email_text(search_data: Dict) -> str:
    return '\n'.join(
        result_data.get('assets', {}).get('preview', {}).get('url', '') for result_data in search_data
    )


def parse_emails_file(filename: str) -> List[str]:
    if not os.path.exists(filename):
        filename = settings.BASE_DIR / 'email_files' / filename

    with open(filename) as file:
        return [line.strip() for line in file.readlines() if line.strip()]  # removes all empty lines


def send_emails(emails: List[str], text: str):
    return requests.post(
        f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages",
        auth=("api", settings.MAILGUN_API_KEY),
        data={"from": f"Excited User <photosearch@{settings.MAILGUN_DOMAIN}>",
              "to": emails,
              "subject": "Search results",
              "text": text
              })
