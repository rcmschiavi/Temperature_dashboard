#!/usr/bin/env pythonproject_folder = os.path.expanduser('~/Temperature_dashboard')
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv

project_folder = os.path.expanduser(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(project_folder, '.env'))

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    # Replace with the following code when in pythonanywhere
    # try:
    #     import pymysql
    #     pymysql.install_as_MySQLdb()
    # except:
    #     pass

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
