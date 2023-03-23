from django.core.management.base import BaseCommand
from django.core.management import call_command

COMMANDS = [
    'load_users',
    'load_category',
    'load_genres',
    'load_titles',
    'load_genre_title',
    'load_reviews',
    'load_comments'
]


class Command(BaseCommand):
    help = 'Загрузка всей базы данных'

    def handle(self, *args, **kwargs):
        for command in COMMANDS:
            call_command(command)
