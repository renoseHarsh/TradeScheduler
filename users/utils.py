import requests

BASE_URL = "https://api-fxpractice.oanda.com"


def get_customer_id(access_token):
    if not access_token:
        return ""
    url = BASE_URL + "/v3/accounts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept-Datetime-Format": "RFC3339",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        return data["accounts"][0]["id"]
    return None
