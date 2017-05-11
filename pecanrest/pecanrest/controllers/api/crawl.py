import requests
from bs4 import BeautifulSoup
from pecan import expose
from pecan.rest import RestController


class CrawlController(RestController):
    @expose('json')
    def index(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        return {'Title': soup.title.string,
                'Page Links': [link.get('href') for link in soup.find_all('a')],
                'Meta Data': [meta.get('name') for meta in soup.find_all('meta')]}
        #'Meta Data': [filter(lambda x: x != 'null', meta.get('name')) for meta in soup.find_all('meta')]
