#!/bin/sh 
queryFile='queryFile'
resultDir='webJson'
mkdir $resultDir
resultCount=5
restart=1
python getWebJsonFromGoogle.py $queryFile $resultDir $resultCount $restart
