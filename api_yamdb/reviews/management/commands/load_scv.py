""" Добавляет management-команду для загрузки данных из csv в модели """
import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User

STATIC_PATH = os.path.join(
    settings.BASE_DIR,
    'static',
    'data'
)

FILES_AND_MODELS = (
    ('category.csv', Category),
    ('genre.csv', Genre),
    ('titles.csv', Title),
    #('genre_title.csv', GenreTitle),
    ('users.csv', User),
    ('review.csv', Review),
    ('comments.csv', Comment),
)

DATA = []

for file, model in FILES_AND_MODELS:
    DATA.append({'path': os.path.join(STATIC_PATH, file), 'model': model})


class Command(BaseCommand):

    def handle(self, *args, **options):
        for i in range(len(DATA)):
            with open(DATA[i]['path']) as f:
                reader = csv.reader(f)
                header = next(reader)
                # print(header)
                for row in reader:
                    DATA[i]['model'].objects.update_or_create(
                        id=row[0],
                        defaults={header[i]: row[i]
                                  for i in range(1, len(header))}
                    )
                self.stdout.write(f'{DATA[i]["path"]} loaded')
