def run():
    from django.conf import settings
    from django.test.utils import get_runner

    runner = get_runner(settings)()
    return runner.run_tests(('mailviews',))


def __main__():
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG)

    sys.exit(run())


if __name__ == '__main__':
    __main__()
