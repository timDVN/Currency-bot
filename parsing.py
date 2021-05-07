import requests
from bs4 import BeautifulSoup

link = 'https://www.cbr.ru/currency_base/daily/'
responce = requests.get(link).text
soup = BeautifulSoup(responce, 'lxml')


def get_rates():
    body = soup.find('body')
    content = body.find('main', id="content")
    td = content.find_all('td')
    for i in range(len(td)):
        td[i] = td[i].text
    for i in range(len(td) // 5):
        td[i * 5 + 4] = (td[i * 5 + 4].replace(',', '.'))
    return td


get_rates()
