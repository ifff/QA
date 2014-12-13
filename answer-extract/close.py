import sys

def extract(queryRaw, candidateRaw, candidateSeg, candidatePos):
    query = queryRaw.readline().strip()
    answerLine = ''
    # pattern case 1
    if query.find(u'下一句') >= 0 or query.find(u'后一句') >= 0 or query.find(u'下半句') >= 0:       
        pos1 = query.find(u'“')
        pos2 = query[pos1+1:].find(u'”')
        queryKey = query[pos1+1:pos2]
        # try split ','
        queryKeyList = queryKey.split('，')
        if len(queryKeyList) > 1: queryKey = queryKeyList[len(queryKeyList) - 1]
        while True:
            candidate = candidateRaw.readline().strip()
            pos = candidate.find(queryKey)
            if pos < 0: continue # not find relevant sentence
            pos += len(queryKey)
            while candidate[pos] == '，' or candidate[pos] == ' ':pos += 1 # pass '，'
            candidateKey = candidate[pos:].split()
            if len(candidateKey) > 1: candidateKey = candidateKey[0]
            candidateKey.replace('。','')
            candidateKey.replace('，','')
            candidateKey.replace('.', '')
            candidateKey.replace(',', '')
            if candidateKey != '':
                # get answer 
                answerLine = candidateKey 
                break
    # pattern case 2    
    elif query.find(u'多少') >= 0:
        while True:
            candidate = candidatePos.readline().strip()
            posList = candidate.split('\t')
            findFlag = False
            for pos in posList:
                wordTag = pos.split()
                if wordTag[1][0] == 'm':
                    # get anwer
                    answerLine = wordTag[0]
                    findFlag = True
            if  findFlag: break
    # pattern case 3
    elif query.find(u'谁') >= 0 or query.find(u'哪位') >= 0:
        while True:
            candidate = candidatePos.readline().strip()
            posList = candidate.split('\t')
            findFlag = False
            for pos in posList:
                wordTag = pos.split()
                if wordTag[1][0] == 'n' and wordTag[1][1] == 'r':                            
                    # get answer 
                    answerLine = wordTag[0] 
                    findFlag = True 
            if  findFlag: break
    # pattern case 4                                                                             
    elif query.find(u'哪个省') >= 0 or query.find(u'哪个市') >= 0 or query.find(u'哪个城市') >= 0 or \
        query.find(u'哪座城市') >= 0 or query.find(u'哪个国家') >= 0 or \
            query.find(u'哪个湖') >= 0 or query.find(u'哪里') >= 0:
        while True:
            candidateList = candidateSeg.readline().strip().split()
            posList = candidatePos.readline().strip().split('\t')
            findFlag = False
            for i in range(0, len(candidateList)):
                candidate = candidateList[i]
                pos = posList[i].split()[1]
                if candidate.find(u'省') >= 0 or candidate.find(u'市') >= 0 or \
                        candidate.find(u'国') >= 0 or \
                            candidate.find(u'哪个湖') >= 0 or candidate.find(u'哪里') >= 0:
                    # write answer 
                    answerLine += candidate + '\n'
                    findFlag = True
                    break
            if findFlag: break
    
    
# main module
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'argv[1]: queryFileDir'
        print 'argv[2]: candidateFileDir'
        print 'argv[3]: answerFileDir'
        exit()

    processID = 1
    answerFile = open(sys.argv[3] + '/close.txt','w')
    while processID <= 15000:
        print 'current process ID ' + str(processID) + '...'
        # load query raw file
        queryRawFile = open(sys.argv[1] + '/' + str(processID),'r')
        # load candidate raw file
        candidateRawFile = open(sys.argv[2] + '/' + str(processID) + '.raw','r')
        candidateSegFile = open(sys.argv[2] + '/' + str(processID) + '.seg','r')
        candidatePosFile = open(sys.argv[2] + '/' + str(processID) + '.pos','r') 
        # open answer file to write
        extract(queryRawFile, candidateRawFile, candidateSegFile, candidatePosFile, answerFile, processID)
        processID += 1

