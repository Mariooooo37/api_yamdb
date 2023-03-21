import csv

from django.core.management.base import BaseCommand

from reviews.models import Title, Category


class Command(BaseCommand):
    help = 'Загрузка Titles'

    def handle(self, *args, **options):
        with open('static/data/titles.csv', encoding="utf8") as File:
            reader = csv.DictReader(File, delimiter=',')
            for row in reader:
                Title.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(id=row['category']),
                )
