#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./webService.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# import SocketServer
import main as base
import backend
# import urllib
import json

def run():
    print 'Starting...'
    file_input = json.load(file("left1.json"))
    # mat=base.np.load('mat.dat')
    maxLength=base.np.load('maxLength.dat')
    # glove = base.load_data('glove.dat')
    # patty = base.load_data('patty.dat')
    # patty.processData()
    mat, glove, patty = backend.processPattyData()#glovePath="../glove.6B.50d.txt",pattyPath='yago-relation-paraphrases_json.txt')
    count = 0
    # i = 14
    file_output = open('testResultLeft'+str(2300)+'.txt','w')
    sumRe = 0
    sumF = 0
    num = 0
    sumPre = 0.0
    for quObj in file_input:
        if count<2100:
            dbrs = []
            facts = []
            factCoun = 0
            # print (i)
            count = count+1
            print count
            print int(quObj['SerialNumber'].encode('ascii'))
            if count%100==0:
            # if count==(i+1)*100
                notHave = 0
                question = quObj['question'].encode('ascii')
                file_output.write("\r\nquestion===============================\r\n")
                file_output.write(question)
                file_output.write('\r\nfacts===============================\r\n')
                entities = quObj['entity mapping']
                factRes = quObj['predicate mapping']
                p = []
                for entity in entities:
                    strE = entity['uri']
                    strE = strE.split('/')[-1]
                    if unicode('C++') in strE:
                        continue
                    # if unicode('Hayden,_Stone_&_Co.') in strE:
                    #     continue
                    # print (strE)
                    dbrs.append(strE)
                for re in factRes:
                    strF = re['uri']
                    # str = str.split('/')[-1]
                    facts.append(strF)
                    file_output.write(strF)
                    file_output.write(',')
                    try :
                        print re['label']
                    except:
                        continue
                    if '@@@' not in re['label'].encode('ascii') and not re['label'].encode('ascii')=='':
                        part = re['label']
                        p.append(part)
                # gparts = p
                try:
                    vectors, parts, pos, gen_question, similarities, unweighted, weighted, result, apiResults,proLin,hidProLin = base.processQuestion(glove,maxLength, patty, mat, question,dbrs,p)
                except:
                    print (sumPre/num)
                    print (sumRe/num)
                    print (sumF/num)
                    print (num)
                    continue
                factLen = len(facts)
                for fact in facts:
                    if fact not in proLin and fact not in hidProLin:
                        factLen = factLen-1
                results = [res[0] for res in result[:factLen]]
                candidates = [res[0] for res in result[:10]]
                o={}
                file_output.write('\r\nresults===============================\r\n')
                o["results"]=results
                o["parts"] = parts
                o["candidates"] = candidates
                for fact in facts:
                    if fact in results:
                        factCoun = factCoun +1
                file_output.write(json.dumps(o, indent=4, sort_keys=True))
                if factLen<1:
                    notHave = notHave+1
                else:
                    num = num+1
                    pFLen = factLen
                    if not factCoun==factLen:
                        bFac = factCoun
                        factCoun = 0
                        reResults = [res[0] for res in result[:factLen+1]]
                        for fact in facts:
                            if fact in reResults:
                                # print (fact)
                                factCoun = factCoun +1
                        if bFac<factCoun:
                            factLen = factLen+1
                        file_output.write("\r\nTest===============================\r\n")
                        file_output.write("F")
                    else:
                        file_output.write("\r\nTest===============================\r\n")
                        file_output.write("T")
                    precision = float(factCoun)/factLen
                    file_output.write("\r\nprecision===============================\r\n")
                    file_output.write(str(precision))
                    recall = float(factCoun)/pFLen
                    file_output.write("\r\nrecall===============================\r\n")
                    file_output.write(str(recall))
                    sf = precision+recall
                    if sf ==0:
                        f = 0
                    else:
                        f = 2*precision*recall/(precision+recall)
                    sumPre = sumPre+precision
                    sumRe = sumRe + recall
                    sumF = sumF+f
                file_output.write('\r\n')
                if count ==2100:
                    print (sumPre/num)
                    print (sumRe/num)
                    print (sumF/num)
                    print (num)
                    file_output.write("\r\nfinal num===============================\r\n")
                    file_output.write(str(num))
                    file_output.write("\r\nfinal sumPre===============================\r\n")
                    file_output.write(str(sumPre))
                    file_output.write("\r\nfinal sumRe===============================\r\n")
                    file_output.write(str(sumRe))
                    file_output.write("\r\nfinal sumF===============================\r\n")
                    file_output.write(str(sumF))
                    # i = i+1
                    # sumRe = 0
                    # sumF = 0
                    # num = 0
                    # sumPre = 0.0
                    # file_output = open('testResultOnlyTest'+str((i+1)*100)+'.txt','w')
                    print 'end!'
                    return
            else:
                continue
                # if count>(i+1)*100 or count==(i+1)*100:
                #     print (sumPre/num)
                #     print (sumRe/num)
                #     print (sumF/num)
                #     print (num)
                #     file_output.write("\r\nfinal num===============================\r\n")
                #     file_output.write(str(num))
                #     file_output.write("\r\nfinal sumPre===============================\r\n")
                #     file_output.write(str(sumPre))
                #     file_output.write("\r\nfinal sumRe===============================\r\n")
                #     file_output.write(str(sumRe))
                #     file_output.write("\r\nfinal sumF===============================\r\n")
                #     file_output.write(str(sumF))
                #     i = i+1
                #     sumRe = 0
                #     sumF = 0
                #     num = 0
                #     sumPre = 0.0
                #     file_output = open('testResultLeft'+str((i+1)*100)+'.txt','w')
                #     print 'end!'
                #     # return
                # else:
                #     continue
        else:
            return

if __name__ == "__main__":
    run()