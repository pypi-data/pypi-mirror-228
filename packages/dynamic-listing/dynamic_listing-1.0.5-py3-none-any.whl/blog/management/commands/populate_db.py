import random

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from blog.factory import CategoryFactory, TagFactory, UserFactory, BlogFactory


class Command(BaseCommand):
    help = 'Updates users table with the aggregated data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start populating blogs data'))
        tags = []
        categories = []
        for i in range(100):
            UserFactory()

        for i in range(20):
            categories.append(CategoryFactory())

        for i in range(30):
            tags.append(TagFactory())

        for user in User.objects.all():
            for b in range(random.randint(1, 10)):
                blog = BlogFactory(author=user, category=random.choice(categories))
                for i in random.sample(tags, random.randint(1, 5)):
                    blog.tags.add(i)

        self.stdout.write(self.style.SUCCESS('End populating blogs data'))
