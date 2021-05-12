import log
import requests
from bs4 import BeautifulSoup

link = 'https://www.cbr.ru/currency_base/daily/'
response = requests.get(link).text
soup = BeautifulSoup(response, 'lxml')


def get_rates():
    log.logger.debug("Function: get_rates.(parsing.py)")
    body = soup.find('body')
    content = body.find('main', id="content")
    td = content.find_all('td')
    for i in range(len(td)):
        td[i] = td[i].text
    for i in range(len(td) // 5):
        # parsing gives list objects like
        # ['036', 'AUD', '1', 'Австралийский доллар', '57.8082', '944', 'AZN', '1','Азербайджанский манат' ...]
        # <code>(never used in bot)   <reduction> <index1> <name>(never used in bot)  <index2>
        td[i * 5 + 4] = (td[i * 5 + 4].replace(',', '.'))  # parsing of <index>
    return td
