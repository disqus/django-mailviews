#!/usr/bin/env python
import logging
import sys

from mailviews.tests import settings


logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    try:
        from django.core.management import execute_manager
        execute_manager(settings)
    except ImportError:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
