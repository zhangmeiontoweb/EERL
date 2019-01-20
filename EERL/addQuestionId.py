#!/usr/bin/env python
# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# import SocketServer
# import main as base
# import urllib
# import json
import csv
# import openpyxl

def run():
    print 'Starting...'
    # file_output = open('addId.csv','w')
    datacsv = open('addIdLc_QUAD.csv','a')
    file_output = csv.writer(datacsv,dialect=("excel"))
    # wb = openpyxl.load_workbook("WSDM_dataset.csv")
    # sheets = wb.get_sheet_names()
    # file_input = wb.get_sheet_by_name(sheets[0])
    file_csv2 = open("questions.csv","r")
    file_csv1 = open("LCQuAD_dataToExcel.csv","r")
    file_input = csv.reader(file_csv2)
    file_input2 = csv.reader(file_csv1)
    for quObj in file_input:
        data = []
        s = str(quObj[1])
        for reObj in file_input2:
            if file_input2.line_num != 1:
                s1 = reObj[0].replace("['","")
                s2 = s1.replace("']","").replace('["',"").replace('"]',"").replace('?',"")
                if s2 !="":
                    # print (s)
                    if s2 in s:
                        # print (s)
                        # print (s2)
                        data.append(quObj[0])
                        data.append(reObj[0])
                        data.append(reObj[1])
                        data.append(reObj[2])
                        data.append(reObj[3])
                        data.append(reObj[4])
    file_output.writerow(data)
    print 'end!'
    return



if __name__ == "__main__":
    run()