from pymongo import MongoClient
import json

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load authors and quotes from database mongodb into the JSON files'

    def handle(self, *args, **kwargs):
        self.get_data("mongodb+srv://itpython2023:Imsheva07*2402@cluster0.vfyc1.mongodb.net/PW-m9-scrapy-project?retryWrites=true&w=majority")
    
    def get_data(self, url):
        # Подключение к MongoDB
        client = MongoClient(url)
        db = client["PW-m9-scrapy-project"]
        quote_collection = db["quote"]
        author_collection = db["author"]

        # Получение всех документов из коллекции
        quotes = quote_collection.find()
        authors = author_collection.find()

        # Преобразование данных в список
        quote_data = list(quotes)
        author_data = list(authors)

        # Сериализация ObjectId в строку
        for element in quote_data:
            element['_id'] = str(element['_id'])
            for author in author_data:
                if element['author']==author['_id']:
                    element['author'] = str(author['fullname'])
            element['tags'] = [tag['name'] for tag in element["tags"]]

        for element in author_data:
            element['_id'] = str(element['_id'])


        # Сохранение в JSON-файл
        with open("quotes.json", "w", encoding="utf-8") as file:
            json.dump(quote_data, file, ensure_ascii=False, indent=4)

        with open("authors.json", "w", encoding="utf-8") as file:
            json.dump(author_data, file, ensure_ascii=False, indent=4)

        # Закрытие подключения
        client.close()

