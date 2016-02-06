from __future__ import unicode_literals

import requests


def ping(event, context):
    """Ping the status of a webpage."""
    options = {
        'domain': 'example.com',
        'protocol': 'http',
        'path': '/',
        'method': 'GET',
        'allow_redirects': False,
        'timeout': 5,
    }
    options.update(event)
    response = requests.request(
        options['method'],
        '{protocol}://{domain}{path}'.format(**options),
        allow_redirects=options['allow_redirects'],
        timeout=options['timeout'])
    response.raise_for_status()
