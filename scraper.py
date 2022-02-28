import requests
from bs4 import BeautifulSoup as BS


def cryptoScrapy(page: int, limit: int):
    url = 'https://coinstats.app/coins/?page=' + str(page) + '&limit=' + str(limit)
    req = requests.get(url)
    html = BS(req.content, 'html.parser')
    cryptos = []
    for crypto in html.select('tbody > tr'):
        rank = int(crypto.select('.rank > a > span')[0].text)
        name = crypto.select('.name > a > div > span')[0].text
        change = crypto.select('.percentChange24h > a > span')[0].get('class')[1]
        change_percent = crypto.select('.percentChange24h > a > span')[0].text
        price = crypto.select('.price > a > span')[0].text
        cryptos.append({
            'rank': rank,
            'name': name,
            'change': change,
            'changePercent': change_percent,
            'price': price
        })
    return cryptos

cryptoScrapy(1, 15)