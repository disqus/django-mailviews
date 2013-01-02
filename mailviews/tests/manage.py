#!/usr/bin/env python
import logging

from django.core.management import execute_manager

from mailviews.previews import autodiscover
from mailviews.tests import settings


logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    autodiscover()
    execute_manager(settings)
