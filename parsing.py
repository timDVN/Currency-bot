import requests
from bs4 import BeautifulSoup

link = 'https://www.cbr.ru/currency_base/daily/'
responce = requests.get(link).text
soup = BeautifulSoup(responce, 'lxml')


def get_rates():
    a1 = soup.find('body')
    a2 = a1.find('main', id="content")
    a3 = a2.find_all('td')
    for i in range(len(a3)):
        a3[i] = a3[i].text
    for i in range(len(a3) // 5):
        a3[i * 5 + 4] = (a3[i * 5 + 4].replace(',', '.'))
    return a3


