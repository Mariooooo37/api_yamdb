import csv

from django.core.management.base import BaseCommand

from reviews.models import Category


class Command(BaseCommand):
    help = 'Загрузка Category'

    def handle(self, *args, **options):
        with open('static/data/category.csv', encoding="utf8") as File:
            reader = csv.DictReader(File, delimiter=',')
            for row in reader:
                Category.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
