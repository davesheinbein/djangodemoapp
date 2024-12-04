#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging

def main():
    """Run administrative tasks."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting manage.py")
    # Set the default settings module for the 'demoproject'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demoproject.settings')
    try:
        # Import the Django command-line utility
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logging.error("Error importing Django", exc_info=True)
        # Raise an error if Django is not installed
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Execute the command-line utility with the provided arguments
    execute_from_command_line(sys.argv)
    logging.info("Finished manage.py")

    if 'runserver' in sys.argv:
        pass

if __name__ == '__main__':
    main()
