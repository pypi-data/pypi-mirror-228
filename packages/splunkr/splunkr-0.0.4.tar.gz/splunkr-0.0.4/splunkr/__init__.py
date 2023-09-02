from splunkr.splunk_http_event_collector import http_event_collector
from copy import deepcopy as dc
import logging

class logg(object):
    def __init__(self, key, host='localhost', popNullFields=True, loggingLevel=logging.DEBUG, index='main'):
        self.mgr = http_event_collector(key, host)

        self.mgr.popNullFields = popNullFields
        self.mgr.log.setLevel(loggingLevel)

        self.basePayload = {
            "index":index
        }

    @property
    def connected(self):
        return self.mgr.check_connectivity()

    def log(self, **keywords):
        current = dc(self.basePayload)
        current['event'] = keywords
        self.mgr.sendEvent(
            current
        )
    
    def __iadd__(self, string):
        self.log(message=string)
        return self