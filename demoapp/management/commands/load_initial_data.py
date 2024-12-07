from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from demoapp.models import Profile, Category, Tag, Article, Author, Book

class Command(BaseCommand):
    help = 'Load initial data into the database'

    def handle(self, *args, **kwargs):
        # Create a superuser
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='Abcde12345!'
            )
            Profile.objects.create(user=admin_user, bio='Admin user profile')

        # Create categories
        category1 = Category.objects.get_or_create(name='Category 1')[0]

        # Create tags
        tag1 = Tag.objects.get_or_create(name='Tag 1')[0]

        # Create articles
        article1 = Article.objects.get_or_create(
            title='Article 1',
            content='Content for article 1',
            category=category1
        )[0]
        article1.tags.add(tag1)

        # Create books
        book1 = Book.objects.get_or_create(
            title='Book 1',
            publication_date='2023-01-01'
        )[0]

        # Create authors
        author1 = Author.objects.get_or_create(name='Author 1')[0]
        author1.books.add(book1)

        self.stdout.write(self.style.SUCCESS('Initial data loaded successfully'))