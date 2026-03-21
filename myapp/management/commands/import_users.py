import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from myapp.models import User  # Replace `User` with your actual model name

class Command(BaseCommand):
    help = 'Imports users from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('users.csv', type=str, help='D:\myproject\users.csv')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                User.objects.create(
                    regno=row['regno'],
                    username=row['username'],
                    email=row['email'],
                    password=make_password(row['password']),  # Hash the password
                    role=row['role']
                    # Add other fields as needed
                )
                self.stdout.write(self.style.SUCCESS(f'Created user: {row["username"]}'))