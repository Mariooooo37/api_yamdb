import csv

from django.core.management.base import BaseCommand

from reviews.models import Review, Category, Title, GenreTitle, Comment, Genre
from user.models import User

MODEL_LINK = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    help = 'Загрузка тестовой БД'

    def handle(self, *args, **options):
        for model, link in MODEL_LINK.items():
            with open(f'static/data/{link}', encoding="utf8") as File:
                reader = csv.DictReader(File, delimiter=',')
                for row in reader:
                    if model == Title:
                        model.objects.get_or_create(
                            id=row['id'],
                            name=row['name'],
                            year=row['year'],
                            category=Category.objects.get(id=row['category']),
                        )
                    elif model == GenreTitle:
                        model.objects.get_or_create(
                            id=row['id'],
                            title=Title.objects.get(id=row['title_id']),
                            genre=Genre.objects.get(id=row['genre_id']),
                        )
                    elif model == Review:
                        model.objects.get_or_create(
                            id=row['id'],
                            title=Title.objects.get(id=row['title_id']),
                            text=row['text'],
                            author=User.objects.get(id=row['author']),
                            score=row['score'],
                            pub_date=row['pub_date'],
                        )
                    elif model == Comment:
                        model.objects.get_or_create(
                            id=row['id'],
                            review=Review.objects.get(id=row['review_id']),
                            text=row['text'],
                            author=User.objects.get(id=row['author']),
                            pub_date=row['pub_date'],
                        )
                    else:
                        model.objects.get_or_create(**row)
