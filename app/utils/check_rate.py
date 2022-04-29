import requests
from bs4 import BeautifulSoup


def check_rates():
    url = "https://www.bestchange.ru/visa-mastercard-uah-to-sberbank.html"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    rates = soup.findAll("td", {"class": "bi"})
    rates_list = []
    for r in rates[0:6]:
        if "uah" in r.text.lower():
            continue
        rate = r.text.split(" ")
        for j in rate:
            if "rub" in j.lower() or "сбербанк" in j.lower():
                continue
            rates_list.append(j)

    rate = (float(rates_list[0]) + float(rates_list[1]) + float(rates_list[2])) / 3
    rate -= rate * 0.02
    return float('{:.2f}'.format(rate))
