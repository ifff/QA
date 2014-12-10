#!/usr/bin/env python
# coding=utf-8
import sys
import simplejson
import urllib2
import urllib
import json

reload(sys)
sys.setdefaultencoding('utf-8')
if len(sys.argv) < 4:
    print 'argv[1]: jsonFile'
    print 'argv[2]: resultFile'
    print 'argv[3]: topN'
    exit()

topN = int(sys.argv[3])
f1 = open(sys.argv[1], 'r')
f2 = open(sys.argv[2], 'w')
while True:
    line1 = f1.readline()
    if not line1:break
    line2 = ''
    # store a json line into file
    tempFile = open('temp', 'w')
    tempFile.write(line1)
    tempFile.close()
    results = json.load(file('temp'))
    count = 0
    for result in results['responseData']['results']:
        count += 1
        if count > topN:break
        for newsinfo in result:
            if newsinfo == 'titleNoFormatting' or newsinfo == 'content':
                line2 += str(result[newsinfo]).replace('\t','').replace('\n','') + '\t'
            #elif newsinfo == 'relatedStories':
            #    for relate in result[newsinfo]:
            #        for term in relate:
            #            if term == 'titleNoFormatting':
            #                line2 += relate[term] + '\t'
    
    line2 +='\n'
    line2 = line2.replace('...','')
    line2 = line2.replace('<b>','')
    line2 = line2.replace('</b>','')
    line2 = line2.replace('&','')
    line2 = line2.replace('#39;','\'')
    line2 = line2.replace('quot;','')   
    f2.write(line2)
f1.close()
f2.close()
