import requests


def fetch_crypto(limit: int, skip: int):
    url = 'https://api.coin-stats.com/v4/coins?limit=' + str(limit) + '&skip=' + str(skip)
    response = requests.get(url)
    return response.json()['coins']
