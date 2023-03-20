from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Загрузка всей базы данных'

    def handle(self, *args, **kwargs):
        call_command('load_users')
        call_command('load_category')
        call_command('load_genres')
        call_command('load_titles')
        call_command('load_genre_title')
        call_command('load_reviews')
        call_command('load_comments')
