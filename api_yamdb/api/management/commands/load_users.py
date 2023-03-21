import csv

from django.core.management.base import BaseCommand

from reviews.models import User


class Command(BaseCommand):
    help = 'Загрузка Users'

    def handle(self, *args, **options):
        with open('static/data/users.csv', encoding="utf8") as File:
            reader = csv.DictReader(File, delimiter=',')
            for row in reader:
                User.objects.get_or_create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                )
