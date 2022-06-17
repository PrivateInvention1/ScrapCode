import requests 
import json
import csv

def get_data():
    url = 'https://www.lifetime.plus/api/analysis2'
    response = requests.get(url)
    #with open('info.json', 'w', encoding='utf=8') as file:
    #    json.dump(response.json(), file, indent=4, ensure_ascii=False)
    categories = response.json()['categories']

    result = []
    for cat in categories:
        category_name = cat.get('name').strip()
        category_items = cat.get('items')
        for item in category_items:
            item_name = item.get('name').strip()
            item_price = item.get('price')
            item_days = item.get('days')
            item_biomaterial = item.get('biomaterial')
            item_description = item.get('description')
            if 'β' in item_description:
                item_description = item_description.replace('β', 'B')
            if 'γ' in item_description:
                item_description = item_description.replace('γ', 'y')
            result.append(
                [category_name, item_name, item_description, item_price, item_days, item_biomaterial]
            )
    with open('result.csv', 'a', encoding='utf=8') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['Категория',
            'Название',
            'Описание',
            'Цена',
            'Готовность в течении',
            'Биоматериал']
        )
        writer.writerows(
            result
        )

def main():
    get_data()

if __name__ == '__main__':
    main()