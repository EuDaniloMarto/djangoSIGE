#!/usr/bin/env python

import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangosige.configs")
    try:
        from django.core.management import execute_from_command_line  # noqa: PLC0415
    except ImportError:
        raise ImportError(  # noqa: B904, TRY003
            "Couldn't import Django. Are you sure it's installed and "  # noqa: EM101
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
