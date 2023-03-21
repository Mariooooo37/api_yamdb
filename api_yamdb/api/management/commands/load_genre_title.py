import csv

from django.core.management.base import BaseCommand

from reviews.models import Genre, Title, GenreTitle


class Command(BaseCommand):
    help = 'Загрузка GenreTitle'

    def handle(self, *args, **options):
        with open('static/data/genre_title.csv', encoding="utf8") as File:
            reader = csv.DictReader(File, delimiter=',')
            for row in reader:
                GenreTitle.objects.get_or_create(
                    id=row['id'],
                    title=Title.objects.get(id=row['title_id']),
                    genre=Genre.objects.get(id=row['genre_id']),
                )
