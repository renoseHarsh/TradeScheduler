import requests

BASE_URL_PAPER = "https://api-fxpractice.oanda.com"
BASE_URL_LIVE = "https://api-fxtrade.oanda.com"


def get_account_ids(access_token, live=False):
    if not access_token:
        return ""
    url = BASE_URL_PAPER + "/v3/accounts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept-Datetime-Format": "RFC3339",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        return data["accounts"]
    return None
