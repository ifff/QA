#!/bin/sh 
queryFile='queryFile'
resultDir='webJson'
mkdir $resultDir
resultCount=5
restart=4
python getWebJsonFromGoogle.py $queryFile $resultDir $resultCount $restart
