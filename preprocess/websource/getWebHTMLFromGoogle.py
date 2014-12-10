# Author:         Fan Feifan
# Email:          fanff.pku@gmail.com
# Filename:       getWebHTMLFromGoogle.py
# Last modified:  2014-08-11 22:42
# Description: get web html from google

import sys
import urllib2
import urllib
import time
import zlib
reload(sys)

if len(sys.argv) < 4:
    print 'argv[1]: queryFile'
    print 'argv[2]: resultFile'
    print 'argv[3]: restart'
    exit()

queryFile = open(sys.argv[1],'r')
resultFile = open(sys.argv[2],'w')
line_count = 0
restartID = int(sys.argv[3])
while True:
    line = queryFile.readline()
    if not line:break
    line_count += 1
    if line_count < restartID:continue
    print 'current qid is ', line_count
    params = {
        'q':line.strip()
    }
    url = 'https://www.google.com/search?' + \
            urllib.urlencode(params) + '&tbs=cdr%3A1%2Ccd_min%3A%2Ccd_max%3A2013%2F3%2F31&tbm='
            #urllib.urlencode(params) + '&newwindow=1&safe=strict&rlz=1C1CHUN_zh-CNCN555CN555&source=lnt&tbs=cdr%3A1%2Ccd_min%3A%2Ccd_max%3A2013%2F3%2F31&tbm='
    print url
    request = urllib2.Request(url)
    request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64)\
                       AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36')
    request.add_header('Accept-encoding','gzip')
    response = urllib2.urlopen(request)
    html = response.read() 
    gzipped = response.headers.get('Content-Encoding')
    if gzipped:
        html = zlib.decompress(html, 16 + zlib.MAX_WBITS)
    resultFile.write(html)
    #time.sleep(3)    
    exit()
queryFile.close()
resultFile.close()
