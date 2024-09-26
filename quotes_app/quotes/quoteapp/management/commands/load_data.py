from django.core.management.base import BaseCommand
from quoteapp.models import Author, Quote, Tag
from datetime import datetime

import json


class Command(BaseCommand):
    help = 'Load authors and quotes from JSON files into the database'

    def handle(self, *args, **kwargs):
        self.load_authors('authors.json')
        self.load_quotes('quotes.json')

    def load_authors(self, file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            authors_data = json.load(file)

        for item in authors_data:
            # born_date = datetime.strptime(item['born_date'], '%Y-%m-%d').date() if item['born_date'] else None
            born_date = item['born_date'] if item['born_date'] else None
            author, created = Author.objects.get_or_create(
                fullname=item['fullname'],
                defaults={
                    'born_date': born_date,
                    'born_location': item['born_location'],
                    'description': item['description']
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added author: {author.fullname}"))

    def load_quotes(self, file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            quotes_data = json.load(file)

        for item in quotes_data:
            author = Author.objects.get(fullname=item['author'])

            quote = Quote.objects.create(
                text=item['quote'],
                author=author
            )

            for tag_name in item['tags']:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                quote.tags.add(tag)

            self.stdout.write(self.style.SUCCESS(f"Successfully added quote: {quote.text[:50]}..."))
