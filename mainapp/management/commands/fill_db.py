import os
import json

from django.core.management.base import BaseCommand

from mainapp.models import Category, Post
from django.conf import settings
from authapp.models import XabrUser


def load_from_json(file_name):
    with open(os.path.join(settings.JSON_PATH, f'{file_name}.json'),
              encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    help = 'Fill DB new data'

    def handle(self, *args, **options):
        categories = load_from_json('categories')

        Category.objects.all().delete()
        [Category.objects.create(**category) for category in categories]

        if not XabrUser.objects.filter(username='django').exists():
            XabrUser.objects.create_superuser(username='django', email='admin@xabr.local', password='geekbrains')

        posts = load_from_json('posts')
        Post.objects.all().delete()  # all() -> QuerySet -> .first() -> concrete object
        for post in posts:
            category_name = post['category']
            _category = Category.objects.get(name=category_name)
            post['category'] = _category
            new_post = Post(**post)
            new_post.save()
