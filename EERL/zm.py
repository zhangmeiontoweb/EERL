#!/usr/bin/env python
#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# import SocketServer
#import main as base
# import urllib
# import json
import csv
# import openpyxl

def run():
    print ('Starting...')
    # file_output = open('addId.csv','w')
    datacsv = open('addId4.csv','a')
    Data = []
    file_output = csv.writer(datacsv,dialect=("excel"))
    with open('questions_5.csv','r') as file_csv2:
        file_input = csv.reader(file_csv2)
        for quObj in file_input:
            s = str(quObj[1])
            data=[]
            with open('QALD-5_dataToExcel.csv','r') as file_csv1:
                file_input2 = csv.reader(file_csv1)
                for reObj in file_input2:
                    if file_input2.line_num != 1:
                        s1 = reObj[1].replace("['","")
                        s2 = s1.replace("']","").replace('["',"").replace('"]',"").replace('?',"")
                        if s2 !="":
                            if s2 in s:
                                # print (s)
                                # print (s2)
                                data.append(quObj[0])
                                data.append(reObj[1])
                                data.append(reObj[2])
                                data.append(reObj[3])
                                data.append(reObj[4])
                                data.append(reObj[5])
                        else:
                            continue
                    else:
                        continue
                Data.append(data)
    file_output.writerows(Data)
    print ('end!')
    return



if __name__ == "__main__":
    run()