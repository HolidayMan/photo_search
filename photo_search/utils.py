import requests
from django.conf import settings


def search_for_images(query: str) -> dict:
    url = f'https://api.shutterstock.com/v2/images/search'
    headers = {'Authorization': f'Bearer {settings.SHUTTERSTOCK_API_TOKEN}'}
    urlparams = {'query': query, 'per_page': 20}
    response = requests.get(url, headers=headers, params=urlparams)
    return response.json()
