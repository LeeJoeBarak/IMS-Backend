#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from utils import get_db_handle, get_collection_handle

DATABASE_NAME = 'IMS-DB'
COLLECTION_NAME = 'IMS-DB'
DATABASE_HOST = 'ISE-IntNet-W36'
DATABASE_PORT = '27017'
USERNAME = 'admin'
PASSWORD = 'mongo1234'

db, client = get_db_handle(DATABASE_NAME,DATABASE_HOST,DATABASE_PORT,USERNAME,USERNAME)

print(db)
print(client)

collection=get_collection_handle(db,"test")
print(collection)

# run env: pipenv shell
# run server in terminal: python manage.py runserver
def main():


    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imsserver.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
