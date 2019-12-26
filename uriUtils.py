from urllib.parse import urlparse


def domainFromUri(uri):
    uri_parsed = urlparse(uri)
    domain = '{uri.netloc}'.format(uri=uri_parsed)
    return domain