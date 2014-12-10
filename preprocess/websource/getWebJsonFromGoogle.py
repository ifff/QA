#!/usr/bin/env python
# coding=utf-8

# get news or web data from google 
import sys
#import simplejson
import urllib2
import urllib
import json
reload(sys)
sys.setdefaultencoding('utf-8')

def searchWeb(query, resultFileName, resultCount):
    resultFile = open(resultFileName, 'w')
    start = 0;
    while start < int(resultCount):
        params = {
            'q':query
        }
        url = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=5&' + \
        urllib.urlencode(params) + '&start=' + str(start);
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        results = json.load(response)
        resultFile.write(json.dumps(results))
        resultFile.write('\n')
        start += 5
    resultFile.close()

if len(sys.argv) < 4:
    print 'sys.argv[1]: queryFile'
    print 'sys.argv[2]: resultDir'
    print 'sys.argv[3]: resultCount'
    print 'sys.argv[4]: restart'
else:
    # read queryFile
    queryFile = open(sys.argv[1],'r')
    line_count = 0
    while True:
        line = queryFile.readline()
        if not line:break
        line_count += 1
        if line_count < int(sys.argv[4]):continue
        query = line.strip().split('\t')
        resultFileName = sys.argv[2] + '/' + str(query[0]) + '.json'
        searchWeb(query[1], resultFileName, int(sys.argv[3]))
        break
    queryFile.close()
