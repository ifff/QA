# Author:         Fan Feifan
# Email:          fanff.pku@gmail.com
# Filename:       readHTML.py
# Last modified:  2014-08-12 09:17
# Description: parse web html search results  

from HTMLParser import HTMLParser
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class stack:
    def __init__(self, size=100):
        self.content = []
        self.msize = size
        self.top = 0
    
    def getTop(self):
        if (self.top > 0):
            return self.content[self.top - 1]
        else: 
            return None

    def getLength(self):
        return len(self.content)

    def push(self, data):
        if (self.top == self.msize):
            return -1
        self.content.append(data)
        self.top = self.top + 1

    def pop(self):
        try:
            res = self.content.pop()
            if (self.top > 0):
                self.top -= 1
            return res
        except IndexError:
            return None

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = ''
        self.topCount = 5
        self.currentCount = 0
        self.st = stack(size='1000')
        self.st.push('start')
    def handle_starttag(self, tag, attrs):
        if tag == 'h3':
            if len(attrs) == 0:pass
            else: self.st.push(tag)
            #print self.st.content
        if tag == 'a' and self.st.getTop() == 'h3':
            #print attrs
            for (variable, value) in attrs:
                #if variable == 'href':
                if variable == 'href' and value.find('http://scholar.google.com') < 0:
                    self.st.push(tag)
                    break
        

        if tag == 'span':
            for (variable, value) in attrs:
                if variable == 'class' and value == 'st':
                    self.st.push(tag)
                    break



    def handle_endtag(self, tag):
        if tag == 'a' and self.st.getTop() == 'a':
            self.st.pop()
        if tag == 'h3' and self.st.getTop() == 'h3':
            self.st.pop()
        if tag == 'span' and self.st.getTop() == 'span':
            self.currentCount += 1
            self.st.pop()
    def handle_data(self, data):
        if self.st.getTop() == 'a' or self.st.getTop() == 'span':
            if self.currentCount < self.topCount: 
                self.result += ' ' + data.replace('\t','').replace('\n','')
            #print data

            #self.links.append(data)
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'argv[1]: htmlFile'
        print 'argv[2]: resultFile'
        exit()

    htmlFile = open(sys.argv[1],'r')
    resultFile = open(sys.argv[2],'w')
    while True:
        line =  htmlFile.readline()
        if not line:break
        parser = MyHTMLParser()
        parser.feed(line.strip())
        parser.close()
    print str(parser.result)
