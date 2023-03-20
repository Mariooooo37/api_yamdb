import csv

from django.core.management.base import BaseCommand

from reviews.models import Comment, Review, User


class Command(BaseCommand):
    help = 'Загрузка Comments'

    def handle(self, *args, **options):
        with open('static/data/comments.csv', encoding="utf8") as File:
            reader = csv.DictReader(File, delimiter=',')
            for row in reader:
                Comment.objects.get_or_create(
                    id=row['id'],
                    review=Review.objects.get(id=row['review_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    pub_date=row['pub_date'],
                )
