from splunkr.splunk_http_event_collector import http_event_collector
from copy import deepcopy as dc
import logging

class logg(object):
    def __init__(self, key, ipaddr='localhost', popNullFields=True, loggingLevel=logging.DEBUG, index='main', host=None, source=None, sourceType=None):
        self.ipaddr = ipaddr
        self.mgr = http_event_collector(key, ipaddr)

        self.mgr.popNullFields = popNullFields
        self.mgr.log.setLevel(loggingLevel)

        self.index = index
        self.basePayload = {
            "index":index
        }

        if host:
            self.basePayload['host'] = host
        if source:
            self.basePayload['source'] = source
        if sourceType:
            self.basePayload['sourceType'] = sourceType

    def link(self, port=8080):
        print("USE SEARCH (index=\"{0}\")| spath message | search **kwargs".format(self.index))
        return "{0}:{1}/en-US/app/search/search?q=search%20(index%253D%22{2}%22)&earliest=rt&latest=rt".format(self.ipaddr, port, self.index)

    @property
    def connected(self):
        return self.mgr.check_connectivity()

    def log(self, event={}, **keywords):
        current = dc(self.basePayload)
        current['event'] = keywords
        self.mgr.sendEvent(
            current
        )
    
    def __iadd__(self, string):
        self.log(message=string)
        return self