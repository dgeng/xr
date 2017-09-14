# Initialize the scroll
import json
import redis
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://10.0.0.10:9200/'])
r = redis.StrictRedis(host='10.0.0.30', port=6379, db=0)

doc = {
    'size' : 10000,
    'query': {
        'match_all' : {}
    }
}

page = es.search(
    index = 'logstash-2017.09.12',
    scroll = '1m',
    body = doc)


def reindex(page):
    hits = page['hits']['hits']
    for each in hits:
        _source = each['_source']
        if '@timestamp' in _source: _source['@timestamp']
        if '@version' in _source: del _source['@version']

        print _source
        payload = json.dumps(_source)
        r.lpush('logstash', payload)

sid = page['_scroll_id']
scroll_size = page['hits']['total']
print "scroll size: " + str(scroll_size)
reindex(page)

# Start scrolling
while (scroll_size > 0):
    print "Scrolling..."
    page = es.scroll(scroll_id=sid, scroll='1m')
    # Update the scroll ID
    sid = page['_scroll_id']
    # Get the number of results that we returned in the last scroll
    scroll_size = len(page['hits']['hits'])
    print "scroll size: " + str(scroll_size)
    reindex(page)
    # Do something with the obtained page
