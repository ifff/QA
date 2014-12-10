#!/usr/bin/env python
# coding=utf-8

# get news or web data from google 
import sys
import simplejson
import urllib2
import urllib
import json
import time
reload(sys)
sys.setdefaultencoding('utf-8')

def getJson(queryFile, resultFile, resultCount, restart):
    f1 = open(sys.argv[1], 'r')
    f2 = open(sys.argv[2], 'a')
    line_count = 0
    restartID = int(restart)
    while True:
        line1 = f1.readline()
        if not line1:break
        line_count +=1
        if line_count < restartID:continue
        print 'current process line: ', line_count
        start = 0;
        while start < int(resultCount):
            params = {
                'q':line1.strip()
            }
            url = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=5&' + \
            urllib.urlencode(params) + '&start=' + str(start);
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            results = simplejson.load(response)
            f2.write(json.dumps(results))
            f2.write('\n')
            start += 5
    f1.close()
    f2.close()

if len(sys.argv) < 4:
    print 'sys.argv[1]: queryFile'
    print 'sys.argv[2]: resultFile'
    print 'sys.argv[3]: resultCount'
    print 'sys.argv[4]: restart'
else:
    getJson(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
