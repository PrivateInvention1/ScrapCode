import requests
from bs4 import BeautifulSoup
import json
import time
import random

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36'
}
number = random.randint(1, 5)
rate = []
urls = []

def get_links():
    page_count = 1
    while True:
        time.sleep(number)
        url = f'https://autodil.com.ua/list/acura/{page_count}/'
        print(page_count)
        page_count += 1
        response = requests.get(url, headers=headers)
        src = response.text
        
        soup = BeautifulSoup(src, 'lxml')

        cards = soup.find_all('div', class_='catalog-card')[1:]
        for card in cards:
            time.sleep(number)
            link = card.find('a', class_='catalog-card__img').get('href')
            for url in urls:
                if link == url:
                    return
            urls.append(link)
            yield link

def get_data():
    for url in get_links():
        time.sleep(number)
        response = requests.get(url, headers=headers)
        src = response.text
        soup = BeautifulSoup(src, 'lxml')

        title = soup.find('h1', class_='product__title').text
        price = soup.find('span', class_='product-total__price').text + 'грн'
        try:
            delivery = soup.find_all('span', class_='product-total__currency')[1].text
        except:
            delivery = 'Стоимость доставки не указана'
        rate.append({
            'Название': title,
            'Цена': price,
            'Доставка': delivery
        })

def main():
    get_data()

if __name__ == '__main__':
    main()
    with open("category.json", "w", encoding="utf=8") as file:
        json.dump(rate, file, indent=4, ensure_ascii=False)

