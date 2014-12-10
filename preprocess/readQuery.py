# Author:         Fan Feifan
# Email:          fanff.pku@gmail.com
# Filename:       readQuery.py
# Last modified:  2014-12-10 14:03
# Description: analysis query file for google web search

#coding:utf8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from xml.etree import ElementTree
if len(sys.argv) < 3:
    print 'argv[1]: queryFile'
    print 'argv[2]: parsedFile'
    exit()

# open parsed File
parsedFile = open(sys.argv[2],'w')
# read query
root = ElementTree.parse(sys.argv[1])
querySet = root.findall('question')
for query in querySet:
    line = query.attrib['id']
    for content in query.getchildren():
        line += '\t' + content.text
        #line = line.decode('utf8')
        parsedFile.write(line+'\n')
        #line = line.encode('gb2312')
        #print line
parsedFile.close()
