from pecan.rest import RestController
from pecanrest.controllers.api.crawl import CrawlController
from pecanrest.controllers.api.time import TimeController


class DemoController(RestController):
    crawl = CrawlController()
    time = TimeController()
