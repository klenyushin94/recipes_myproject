import csv

from django.core.management.base import BaseCommand
from backend.foodgram.recipes.models import Ingredients


class Command(BaseCommand):
    help = 'Import ingredients from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Пропустить заголовки столбцов

            for row in reader:
                name = row[0]
                unit = row[1]
                ingredient = Ingredients(name=name, unit=unit)
                ingredient.save()

        self.stdout.write(
            self.style.SUCCESS('Ingredients imported successfully')
        )
