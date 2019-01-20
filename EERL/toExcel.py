import csv
import re
def doExcel():
    print 'Starting...'
    e = 1
    datacsv = open('WWW_LC_QUAD_left dataset.csv','w')
    csvwriter = csv.writer(datacsv,dialect=("excel"))
    # file_input = json.load(file("Evaluation results/baseline-qald7-eval.csv"))
    while e<24:
        # mainfileH = open("testResultOnlyTest"+str(e*100)+".txt","r")
        mainfileH = open("testResultLeft"+str(e*100)+".txt","r")
        i = 0
        data = dict()
        sdata = dict()
        num = dict()
        data[0] = []
        sdata[0] = ''
        num[0] = 0
        for line in mainfileH.readlines():
            line = line.strip('\r\n')
            if line.isdigit():
                if int(line)>i:
                    i = i+1
                    num[i]=line
                    data[i] = []
                    sdata[i] = ''
                    continue
                else:
                    data[i].append(line)
                    sdata[i] = sdata[i]+line
            else:
                data[i].append(line)
                sdata[i] = sdata[i]+line
        ndata = dict()

        for row in data:
            a = -1
            b = -1
            c = -1
            d = -1
            ndata[row] = []
            ndata[row].append(str(num[row]))
            for s in data[row]:
                if "question" in s:
                    a=data[row].index(s)
                if "facts" in s:
                    b=data[row].index(s)
                if "precision" in s:
                    c = data[row].index(s)
                if "recall" in s:
                    d = data[row].index(s)
            if a>-1:
                ndata[row].append([x for i,x in enumerate(data[row]) if i == a+1])
            else:
                ndata[row].append('')
            if b>-1:
                ndata[row].append([x for i,x in enumerate(data[row]) if i == b+1])
            else:
                ndata[row].append('')
            ndata[row].append(str(re.findall('"results":(.*)}Test',sdata[row])))
            if c>-1:
                ndata[row].append([x for i,x in enumerate(data[row]) if i == c+1])
            else:
                ndata[row].append('')
            if d>-1:
                ndata[row].append([x for i,x in enumerate(data[row]) if i == d+1])
            else:
                ndata[row].append('')
            csvwriter.writerow(ndata[row])
        e = e+1
if __name__ == "__main__":
    doExcel()