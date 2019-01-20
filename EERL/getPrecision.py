#!/usr/bin/env python
#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# import SocketServer
#import main as base
# import urllib
import json
import csv
# import openpyxl

def run():
    print ('Starting...')
    # file_output = open('addId.csv','w')
    # datacsv = open('addId4.csv','a')
    Data = []
    # file_output = csv.writer(datacsv,dialect=("excel"))
    pre = 0
    sumN = 0
    with open('q-5-out.txt','r') as file2:
        # file_input = csv.reader(file_csv2)
        index = 0
        for quObj in file2.readlines():
            s = json.loads(quObj)
            sre=[]
            for rank in s["rerankedlists"]:
                # print str(s["rerankedlists"][rank][0]).replace("[","").replace("]","").replace("u'","").replace("'","").split(",")[1]
                if len(s["rerankedlists"][rank])>2:
                    sre.append(str(s["rerankedlists"][rank][0]).replace("[","").replace("]","").replace("u'","").replace("'","").replace(" ","").split(",")[1])
                    sre.append(str(s["rerankedlists"][rank][1]).replace("[","").replace("]","").replace("u'","").replace("'","").replace(" ","").split(",")[1])
                    sre.append(str(s["rerankedlists"][rank][2]).replace("[","").replace("]","").replace("u'","").replace("'","").replace(" ","").split(",")[1])
                else:
                    if len(s["rerankedlists"][rank])>1:
                        sre.append(str(s["rerankedlists"][rank][0]).replace("[","").replace("]","").replace("u'","").replace("'","").replace(" ","").split(",")[1])
                        sre.append(str(s["rerankedlists"][rank][1]).replace("[","").replace("]","").replace("u'","").replace("'","").replace(" ","").split(",")[1])
                    else:
                        if len(s["rerankedlists"][rank])>0:
                            sre.append(str(s["rerankedlists"][rank][0]).replace("[","").replace("]","").replace("u'","").replace("'","").replace(" ","").split(",")[1])

            index = index + 1
            print sre
            with open('QALD-5_dataToExcel.csv','r') as file_csv1:
                file_input2 = csv.reader(file_csv1)
                count = 0
                for reObj in file_input2:
                    if count==index:
                        re =  reObj[2].replace('["',"").replace('"]',"").replace("[","").replace("]","").replace("'","").split(",")
                        rec = 0
                        if len(re)>0:
                            sumN = sumN + 1
                            print re
                            for result in re:
                                # print result
                                if result in sre:
                                    rec = rec + 1
                            p = float(rec)/len(re)
                            pre = pre + p
                            print p
                        break
                    else:
                        count = count + 1
                        continue

                # for reObj in file_input2:
                #     if file_input2.line_num != 1:
                #         s1 = reObj[1].replace("['","")
                #         s2 = s1.replace("']","").replace('["',"").replace('"]',"").replace('?',"")
                #         if s2 !="":
                #             if s2 in s:
                #                 # print (s)
                #                 # print (s2)
                #                 data.append(quObj[0])
                #                 data.append(reObj[1])
                #                 data.append(reObj[2])
                #                 data.append(reObj[3])
                #                 data.append(reObj[4])
                #                 data.append(reObj[5])
                #         else:
                #             continue
                #     else:
                #         continue
                # Data.append(data)
    # file_output.writerows(Data)
    print (float(pre)/sumN)
    print ('end!')
    return



if __name__ == "__main__":
    run()