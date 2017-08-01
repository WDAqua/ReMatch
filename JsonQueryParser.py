#!/usr/bin/env python
"""This program execute
   Run:
   $ python JsonQueryParser.py qald-file.json

"""
import sys
import json
import os
import unicodedata
import re
from collections import defaultdict

pattern = "http://dbpedia.org/ontology"
pattern2 = "dbo:"
class QueryDataBase(object):
    def __init__(self, inputfilepath):
        self.inputfilepath = inputfilepath
        self.database=defaultdict(list)

    def openFile(self):
        if os.path.exists(self.inputfilepath):
            with open(self.inputfilepath, 'r') as inputfile:
                try:
                    tmpinputdata = json.loads(inputfile.read())
                    inputfile.close()
                    return tmpinputdata
                except IOError:
                    print "Error :Input file read or open error "
                    sys.exit()
                except TypeError:
                    print "Error :Input file json error "
                    sys.exit()
        else:
            print "Error :File path does not exist"
            sys.exit()

    def patternList(self, tmpStr):
         tmplist = tmpStr.split(" ")
         filterlist = []
         for i in range (0, len(tmplist)):
             if pattern2 in tmplist[i]:
                  matchObj = re.match( 'dbo:.+', tmplist[i], re.M|re.I)
                  if matchObj:
                      filterlist.append(matchObj.group()[4:])
             elif pattern in tmplist[i]:
                 matchObj = re.match( '<http://dbpedia.org/ontology/.+>', tmplist[i], re.M|re.I)
                 if matchObj:
                     filterlist.append(tmplist[i][29:-1])         
         return filterlist


    def createDataBase(self, inputData) :
        
        if inputData['dataset']['id'] == 'qald-6-train-multilingual' :
        
            for id in range (0, len(inputData['questions'])):
                if "en" == str(inputData['questions'][id]['question'][0]['language']):
                    tmpQue = inputData['questions'][id]['question'][0]['string']
                    tmpQue_str = (unicodedata.normalize('NFKD', tmpQue).encode('ascii','ignore')).upper()
                    if inputData['questions'][id]['query'].has_key('sparql'):
                        try:
                            self.database[tmpQue_str] = self.patternList(str(inputData['questions'][id]['query']['sparql']))
                        except:
                            self.database[tmpQue_str] = []
                    else:
                        self.database[tmpQue_str] = []
        
        elif inputData['dataset']['id'] == 'qald-5_train' :
        
            for id in range (0, len(inputData['questions'])) :
                if "en" == str(inputData['questions'][id]['body'][0]['language']) :
                    tmpQue = inputData['questions'][id]['body'][0]['string']
                    tmpQue_str = (unicodedata.normalize('NFKD', tmpQue).encode('ascii','ignore')).upper()
               
                    # some entries do not have query
                    if 'query' in inputData['questions'][id]:
                        try:
                            self.database[tmpQue_str] = self.patternList(str(inputData['questions'][id]['query']))
                        except:
                            self.database[tmpQue_str] = []
                    else:
                        self.database[tmpQue_str] = []
        
        else :
            print "Invalid QALD dataset key"
    
    
    def getQueryResult(self, query):
        precision = 0.0
        count = 0.0
        
        if query in self.database.keys():
            print "Query Found !!"
            uriQueryList = self.user_input_uri_list()
            checkList = self.database[query]
            
            if len(checkList) > 0 :
                for i in uriQueryList:
                    if i in checkList:
                        count += 1.0
                
                precision = count/len(checkList)
        else:
            print "Query Not Found !!!!!"

        return precision


    def user_input_uri_list(self):
        count = int(raw_input("Type count:").rstrip())

        uriQueryList = []

        for i in range(0, count):
            tmp_uri = raw_input("Type Uri  :").rstrip()
            uriQueryList.append(tmp_uri.lower())

        return uriQueryList

    def print_result(self, query, precision):

        print "\nResult for " + query + " ."
        print "Precision: ", precision


def main():
    
    if len(sys.argv) > 1 :
        inputfilepath = sys.argv[1]
    else :
        print "Usage: $ python JsonQueryParser.py qald-file.json"
        return 1

    print "Example :"
    print "Type Query: What is the birth name of Angela Merkel?"
    print "Type count: 2"
    print "Type Uri  : <http://dbpedia.org/ontology/birthName>\n\n"

    #inputfilepath = "qald-6-train-multilingual.json"
    #inputfilepath = "qald-5_train.json"
    
    queryDataBase = QueryDataBase(inputfilepath)
    inputData = queryDataBase.openFile()
    queryDataBase.createDataBase(inputData)

    while True:
        query = raw_input("Type Query:").rstrip()

        precision = queryDataBase.getQueryResult(query.upper())

        queryDataBase.print_result(query, precision)

        keyinput = raw_input("Please Enter Y for Continue or any other to stop ===>")

        if "y" != keyinput.lower():
            break





if __name__ == "__main__":
    main()
