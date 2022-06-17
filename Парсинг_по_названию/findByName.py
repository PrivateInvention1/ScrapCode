import requests 
from bs4 import BeautifulSoup
import time
import random
import json

url = 'https://rusbesedka.ru/produktsiia/besedki-dlya-dachi/'
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36"
}

def get_data():
    response = requests.get(url, headers=headers)
    with open('index.html', 'w', encoding='utf=8') as file:
        file.write(response.text)
    with open('index.html', encoding='utf=8') as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')

    cards = soup.find_all('div', class_='product-card')[1:]

    categories = [
        'Восьмигранная',
        'Шестигранная',
        'Прямоугольная',
        'Квадратная',
        'Застекленная',
        'Закрытая',
        'с барбекю',
        'Гриль',
        'Двухэтажная',
        'Овальная',
        'Японская',
        'Угловая',
        'с кроватью',
        'Оригинальная',
        'Современная',
        'Премиум',
        'из минибруса'
    ]
    data = []
    for category in categories:
        for card in cards:
            title = card.find('p', class_='product-card__title').text
            if category in title:
                try:
                    price = card.find('span', class_='is-size-4').next_element.text + 'руб.'
                except:
                    price = card.find('div', class_='product-card__info').find_all('p')[-1].text
                try:
                    size = card.find('p', class_='is-size-7').find('span').text
                except:
                    size = 'Длина не указана'
                try:
                    square = card.find('span', class_='is-size-7').next_element.text
                except:
                    square = 'Площадь не указана'
                href = 'https://rusbesedka.ru' + card.find('a', class_='product-card__link').get('href')
                r = requests.get(href, headers=headers)
                src = r.text
                soup = BeautifulSoup(src, 'lxml')
                try:
                    descrption = soup.find('div', class_='columns is-hidden-touch').find('p', class_='is-size-5').text
                except:
                    descrption = "Описание отсутствует"
                data.append(
                    {
                        'Название': title,
                        'Ссылка': href,
                        'Цена': price,
                        'Длина': size,
                        'Площадь': square,
                        'Описание': descrption
                    }
                )
                print(title)
        with open(f'{category}.json', 'w', encoding='utf=8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        data.clear()
def main():
    get_data()
if __name__ == '__main__':
    main()