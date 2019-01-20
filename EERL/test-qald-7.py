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
# import urllib
import json
import csv
# from future import division
# import urlparse
# import utils

# class S(BaseHTTPRequestHandler):
#
#     initialized = False
#
#     def init(self):
#         if not self.initialized:
#             self.initialized = True
#             print('init started')
#             self.mat=base.np.load('mat.dat')
#             self.maxLength=base.np.load('maxLength.dat')
#             self.glove = base.load_data('glove.dat')
#             self.patty = base.load_data('patty.dat')
#             self.patty.processData()
#             print("data loaded")
#

#
#     def _set_headers(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'application/json')
#         self.end_headers()
#
#     def do_GET(self):
#         if not '.' in self.path[-4:]:
#             self.init()
#             self._set_headers()
#
#             arr = dict(urlparse.parse_qsl(urlparse.urlsplit(self.path).query))
#             print(arr)
#             question = urllib.unquote(arr["q"])
#             Dstr = urllib.unquote(arr["d"])
#             print(question)
#             print (Dstr)
#             dbrs = Dstr.split('>')
#             #self.wfile.write("<html><body><h1>"+question+"</h1></body></html>")
#             vectors, parts, pos, gen_question, similarities, unweighted, weighted, result, apiResults = base.processQuestion(self.glove,self.maxLength, self.patty, self.mat, question,dbrs)
#             o={}
#             #o["vectors"]=[]
#             #for vec in vectors:
#             #	o["vectors"].append(vec.tolist())
#             o["parts"]=parts
#             o["pos"]=pos
#             o["question"]=question
#             o["gen_question"]=gen_question
#             results = [res[0] for res in result[:10]]
#             if apiResults:
#                 i = 0
#                 for part in parts:
#                     key = 'relation %d' % (i+1)
#                     o[key] = results[i]
#                     i += 1
#             o["results"]=results
#             self.wfile.write(json.dumps(o, indent=4, sort_keys=True))
#
#     def do_HEAD(self):
#         self._set_headers()
#
#     def do_POST(self):
#         content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
#         post_data = self.rfile.read(content_length) # <--- Gets the data itself
#         print post_data # <-- Print post data
#         self._set_headers()

def run():
    print 'Starting...'
    file_output = open('testResultTop1-100_QALD-7.txt','w')
    # file_input = json.load(file("Evaluation results/baseline-qald7-eval.csv"))
    file_csv = open("Evaluation results/data-qald7-eval.csv","r")
    file_input = csv.reader(file_csv)
    maxLength=base.np.load('maxLength.dat')
    mat=base.np.load('mat.dat')
    glove = base.load_data('glove.dat')
    patty = base.load_data('patty.dat')
    patty.processData()
    sumPre = 0
    sumRe = 0
    sumFCount = 0
    sumCCount = 0
    sumRCount = 0
    sumF = 0
    num = 0
    sumPre = 0.0
    sumCall = 0.0
    notHave = 0
    count = 0
    pFLen = 0
    for quObj in file_input:
        if file_input.line_num == 1:
            continue
        question = quObj[0]
        facts = quObj[1].split('/')
        dbrs = quObj[2].split('/')
        if count<50:
            # dbrs = []
            # facts = []
            factCoun = 0
            count = count+1
            if not count<0:
                file_output.write("\r\nquestion===============================\r\n")
                file_output.write(question)
                file_output.write('\r\nfacts===============================\r\n')
                file_output.write(str(facts))
                print (count)
                print (dbrs)
                vectors, parts, pos, gen_question, similarities, unweighted, weighted, result, apiResults,proLin,hidProLin = base.processQuestion(glove,maxLength, patty, mat, question,dbrs)
                factLen = len(facts)
                # for fact in facts:
                #     if fact not in proLin and fact not in hidProLin:
                #         factLen = factLen-1
                results = [res[0] for res in result[:factLen]]
                candidates = [res[0] for res in result[:10]]
                reResults = [res[0] for res in result[:factLen+1]]
                o={}
                file_output.write('\r\nresults===============================\r\n')
                o["results"]=results
                o["parts"] = parts
                o["candidates"] = candidates
                comRe = []
                for result in results:
                    result = result.split('/')[-1]
                    if not result in comRe:
                        comRe.append(result)
                # print (comRe)
                for fact in facts:
                    if fact in comRe:
                        # print (fact)
                        factCoun = factCoun +1

                # print (factCoun)
                # print (len(facts))
                file_output.write(json.dumps(o, indent=4, sort_keys=True))
                if factLen<1:
                    notHave = notHave+1
                else:
                    # sumFCount = sumFCount + factLen
                    num = num+1
                    pFLen = factLen
                    # precision = float(factCoun)/factLen
                    # print (precision)
                    # print (factCoun)
                    # print (factLen)
                    if not factCoun==factLen:
                        bFac = factCoun
                        factCoun = 0

                        comReRe = []
                        # print (reResults)
                        for result in reResults:
                            result = result.split('/')[-1]
                            if not result in comReRe:
                                comReRe.append(result)
                        # print (comReRe)
                        for fact in facts:
                            if fact in comReRe:
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
                    recall = float(factCoun)/pFLen
                    # f = 2*precision*recall/(precision+recall)

                    # sumCCount = sumCCount +factCoun
                    # sumRCount = sumRCount+ factLen

                    sumPre = sumPre+precision
                    sumRe = sumRe + recall
                    # sumF = sumF+f
                    # if factCoun>0:
                    # recall = float(factCoun)/len(facts)
                    # sumCall = sumCall+ recall
                    # if precision ==0 and recall==0:
                    #     f = 0
                    # else:
                    #     f = 2*precision*recall/(precision+recall)
                    # sumF = sumF + f
                file_output.write('\r\n')
                # count+=1
        else:
            # precision = float(sumCCount)/sumRCount
            # recall = float(sumCCount)/sumFCount
            # f = 2*precision*recall/(precision+recall)
            # print (sumFCount)
            # print (sumCCount)
            # print (sumRCount)
            # print (precision)
            # print (recall)
            # print (f)
            print (sumPre/num)
            print (sumRe/num)
            print (sumPre)
            print (sumRe)
            print (num)
            # print (sumF/num)

            print 'end!'
            return



if __name__ == "__main__":
    run()