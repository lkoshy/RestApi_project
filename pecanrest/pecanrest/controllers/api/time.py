import strict_rfc3339
from pecan import expose
from pecan.rest import RestController
import time


class TimeController(RestController):
    @expose('json')
    def index(self):
        current_time = int(time.time() * 1000)
        return {'System time': strict_rfc3339.now_to_rfc3339_localoffset(current_time)}
