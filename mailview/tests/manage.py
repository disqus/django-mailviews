#!/usr/bin/env python
from django.core.management import execute_manager

from mailview.tests import settings

if __name__ == "__main__":
    execute_manager(settings)
