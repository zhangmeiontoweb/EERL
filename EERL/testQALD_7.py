# -*- coding: utf-8 -*-
#!/usr/bin/env python

import main as base
import backend
import json
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')
def run():
    print 'Starting...'
    file_input = json.load(file("qald-7-train-multilingual.json"))
    maxLength=base.np.load('maxLength.dat')
    # mat=base.np.load('mat.dat')
    # glove = base.load_data('glove.dat')
    # patty = base.load_data('patty.dat')
    # patty.processData()
    mat, glove, patty = backend.processPattyData()#glovePath="../glove.6B.50d.txt",pattyPath='yago-relation-paraphrases_json.txt')
    count = -1
    file_output = open('test_7_300_parts.txt','w')
    sumRe = 0
    sumF = 0
    num = 0
    sumPre = 0.0
    i=2
    for quObj in file_input["questions"]:
        if count<215:
            dbrs = []
            facts = []
            factCoun = 0
            count = int(quObj['id'].encode('ascii'))
            # if count==112:
            #     continue
            # if count==165:
            #     continue
            # if count==177:
            #     continue
            # if count==187:
            #     continue
            # if count==23:
            #     continue
            # if count==60:
            #     continue
            # if count==81:
            #     continue
            # if count>180:
            if count>i*100:
                notHave = 0
                question = quObj['question'][0]['string']
                file_output.write(str(count))
                file_output.write("\r\nquestion===============================\r\n")
                file_output.write(question)
                file_output.write('\r\nfacts===============================\r\n')
                keywords = quObj['question'][0]['keywords']
                query = quObj['query']['sparql'].replace('\n','').replace('\t','')
                if 'UNION' in query:
                    continue
                if 'FILTER' in query:
                    continue
                sparqls = str(re.findall('WHERE {(.*)}',query)).replace("[u'","").replace("']","").split(' .')
                print (count)
                # print (str(re.findall('WHERE {(.*)}',query)).replace("['","").replace("']",""))
                # print (sparqls)
                p = []
                fdbrs =[]
                edbrs=[]
                for sparql in sparqls:
                    if len(sparql.replace(" ","").replace("u'",""))>0:
                        fdbrs.append([x for x in sparql.split(' ') if x!=''][1])
                        edbrs.append([x for x in sparql.split(' ') if x!=''][0])
                        edbrs.append([x for x in sparql.split(' ') if x!=''][2])
                # print (edbrs)
                for ss in edbrs:
                    if ss.startswith("<"):
                        ss1 = ss.split('/')[-1]
                        dbrs.append(str(ss1).replace(">",""))
                    if ss.startswith("res"):
                        dbrs.append(ss.replace("res:",""))
                    if ss.startswith("dbo"):
                        dbrs.append(ss.replace("dbo:",""))
                # print (dbrs)
                for ss in fdbrs:
                    if ss.startswith("dbo"):
                        ss1 = ss.replace("dbo:","")
                        facts.append("http://dbpedia.org/ontology/"+ss1+"")
                    if ss.startswith("dbp"):
                        ss1 = ss.replace("dbp:","")
                        facts.append("http://dbpedia.org/property/"+ss1+"")
                    if ss.startswith("res"):
                        ss1 = ss.replace("res:","")
                        facts.append("http://dbpedia.org/resource/"+ss1+"")
                    if ss.startswith("rdf"):
                        ss1 = ss.replace("rdf:","")
                        facts.append("http://www.w3.org/1999/02/22-rdf-syntax-ns#"+ss1+"")
                    if ss.startswith("<"):
                        facts.append(ss[1:len(ss)-1])
                # print (facts)
                file_output.write(str(facts))
                p = keywords.split(', ')
                vectors, parts, pos, gen_question, similarities, unweighted, weighted, result, apiResults,proLin,hidProLin = base.processQuestion(glove,maxLength, patty, mat, question,dbrs,p)
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
                if count==214:
                    print (num)
                    print (sumPre/num)
                    print (sumRe/num)
                    print (sumF/num)
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
                if count<i*100+1:
                # if count<181:
                    continue
                else:
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
        else:
            return

if __name__ == "__main__":
    run()