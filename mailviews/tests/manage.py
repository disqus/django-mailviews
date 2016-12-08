#!/usr/bin/env python
import logging
import sys

from mailviews.tests import settings


logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
