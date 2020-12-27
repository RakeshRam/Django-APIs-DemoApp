from django.core.management.base import BaseCommand
from core.models import ExtendUser

from util.fake_data_creator import create_awards, create_awards_records 
from util.fake_data_creator import create_publishers, create_authors, create_books

# python manage.py setup_dummydata
class Command(BaseCommand):
    help = 'Creates Dummy Data'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('-su', '--superuser', type=str, help='Create super user[y/n]', )

    def handle(self, *args, **kwargs):
        if kwargs.get('superuser') != "n":
            self.stdout.write("Creating SuperUser")
            user = ExtendUser.objects.create_user('admin', password='admin')
            user.is_superuser=True
            user.is_staff=True
            user.save()
            self.stdout.write("Done - Creating SuperUser")

        self.stdout.write("Creating Dummy Data for Testing")
        create_awards()
        create_awards_records()
        create_publishers()
        create_authors()
        create_books()
        self.stdout.write("Done - Dummy Data Created")