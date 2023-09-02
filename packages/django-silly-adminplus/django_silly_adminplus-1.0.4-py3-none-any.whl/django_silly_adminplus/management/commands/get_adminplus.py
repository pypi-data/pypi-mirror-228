import os
import shutil
from pathlib import Path

from django.core.management.base import BaseCommand


DSAP_DIR = Path(__file__).resolve().parent.parent.parent


class Command(BaseCommand):
    """Django command to get the application _adminplus installed in the project"""

    def handle(self, *args, **options):

        from_directory = os.path.join(DSAP_DIR, "plop/adminplus/_adminplus")
        shutil.copytree(
            from_directory, os.path.join(os.getcwd(), '_adminplus'))

        print(
            "_adminplus application added, check the wiki to finalize: \n"
            "https://github.com/byoso/django-silly-adminplus/wiki\n"
            )
