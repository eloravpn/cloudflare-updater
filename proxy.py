import os


def load_proxy():
    proxy = 'http://localhost:1090'

    os.environ['http_proxy'] = proxy

    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy
