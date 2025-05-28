import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin


class PageNotFoundError(Exception):
    pass

def get_response(url: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise PageNotFoundError(f"Страница не найдена (код {response.status_code})")

def parse_animals_page(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    
    animal_groups = soup.find_all('div', class_='mw-category-group')
    
    animals = []
    for group in animal_groups:
        letter = group.find('h3').text
        for a in group.find_all('a'):
            animals.append(f"{letter} - {a.text}")
    
    next_page = soup.find('a', text='Следующая страница')
    next_url = urljoin('https://ru.wikipedia.org', next_page['href']) if next_page else None
    
    return animals, next_url

def save_to_csv(data: list, filename: str = 'animals.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Животное'])
        writer.writerows([[animal] for animal in data])

def main():
    base_url = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
    all_animals = []
    
    try:
        url = base_url
        while url:
            print(f"Обрабатываю: {url}")
            html = get_response(url)
            animals, url = parse_animals_page(html)
            all_animals.extend(animals)
        
        save_to_csv(all_animals)
        print(f"Сохранено {len(all_animals)} животных в animals.csv")
    
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    main()