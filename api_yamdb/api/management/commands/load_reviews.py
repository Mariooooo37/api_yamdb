import csv

from django.core.management.base import BaseCommand

from reviews.models import Review, User, Title


class Command(BaseCommand):
    help = 'Загрузка Reviews'

    def handle(self, *args, **options):
        with open('static/data/review.csv', encoding="utf8") as File:
            reader = csv.DictReader(File, delimiter=',')
            for row in reader:
                Review.objects.get_or_create(
                    id=row['id'],
                    title=Title.objects.get(id=row['title_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
