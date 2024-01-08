from csv import DictReader
from django.core.management import BaseCommand

# Import the model
from basket.models import Products

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the flag data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from product_list.csv"

    def handle(self, *args, **options):

        # Show this if the data already exist in the database
        if Products.objects.exists():
            print('product data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading product data")

        # Code to load the data into database
        with open('basket/source_files/product_list.csv', 'r', encoding='1250') as file:
            for row in DictReader(file, delimiter=','):

                product = Products(name=row['name'],
                                   price=row['price'],
                                   category_id=row['category_id'],
                                   description=row['description'],
                                   image=row['image'])
                product.save()


