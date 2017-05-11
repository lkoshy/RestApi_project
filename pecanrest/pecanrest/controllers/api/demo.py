import strict_rfc3339
import requests
import time
from bs4 import BeautifulSoup
from pecan import expose, abort
from pecan.rest import RestController


_STATUS_MAP = {}


def update_hit_list(url, links):
    """
    Updates the global map with the count of requests handled and how many links it has found on web pages

    Args:
        url: The URL name
        links: List of links in the visited web page

    """
    if 'requests handled' in _STATUS_MAP:
        _STATUS_MAP['requests handled'] += 1
    else:
        _STATUS_MAP['requests handled'] = 1
    _STATUS_MAP.update({url: 'links => %s' % len(links)})


def get_response(url):
    """ Gets an URL

    Args:
        url: The URL to be accessed

    Returns:
        a response object
    """
    try:
        response = requests.get(url, timeout=5)
    except requests.Timeout as e:
        raise Exception('HTTP Response Timeout: %s' % e.message)

    return response


class CrawlController(RestController):
    """
    To fetch a given URL and determine the page title, meta data, and links on it
    """
    @expose('json')
    def index(self, **kwargs):

        # Validate the URL key.
        if len(kwargs) > 1 and 'url' not in kwargs:
            abort(400, 'Either Invalid number of keys or Missing URL key')

        # Get the response
        url = kwargs['url']
        response = get_response(url)

        if not response or response.status_code != 200:
            raise Exception('HTTP Response Not OK. Response code: %s' % response.status_code)

        soup = BeautifulSoup(response.text, 'html.parser')
        page_links = [link.get('href') for link in soup.find_all('a')]

        update_hit_list(url, page_links)

        return {'Title': soup.title.string,
                'Page Links': page_links,
                'Meta Data': [meta.get('name') for meta in soup.find_all('meta')]}


class StatusController:
    """
    Reports the current status of the API application.
    """
    @expose('json')
    def index(self):
        return _STATUS_MAP if _STATUS_MAP else 'Nothing to display'


class TimeController:
    """
    Displays the current system time in RFC3339 format
    """
    @expose('json')
    def index(self):
        current_time = int(time.time() * 1000)
        return {'System time': strict_rfc3339.now_to_rfc3339_localoffset(current_time)}


class DemoController(RestController):
    """
    Router to crawl, time an status endpoints
    """
    crawl = CrawlController()
    time = TimeController()
    status = StatusController()
