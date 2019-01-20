# -*- coding: utf-8 -*-
# main file

# ===== imports =====
from __future__ import print_function
import frontend
import backend
import utils
import numpy as np
# import JsonQueryParser as qald
import cPickle  as pickle
# from distance import levenshtein as dist
# import csv
import jpype
import os
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')
# ======= consts =============

''' number of winner relations for each part of the question '''
NUM_WINNERS = 35

''' minimum length of combinatorials of the question'''
MIN_LENGTH_COMP = 2

''' maximum length of combinatorials of the question'''
MAX_LENGTH_COMP = 3

''' threshold for taking winners '''
THRESHOLD = 0.89

''' apply the penitly style '''
APPLY_PENILTY = True

''' use text razor api to get relations '''
USE_TEXT_RAZOR = True

''' apply the synonyms style '''
USE_SYNONYMS = False


# ===== definitions =====

def readQuestion():
    #return 'Who is the wife of Obama'
    #return 'as president'
    #return 'child of'
    #return 'To whom Barack Obama is married to'
    #return 'On which team does Ronaldo plays'
    #return 'With which team did Ronaldo plays ten games for'
    #return 'In which country was Beethoven born'
    #return 'which river flows through Bonn'
    #return 'Give me all actors who were born in Paris after 1950.'
    #return 'where in France is sparkling Wine produced'
    #return 'who was named as president of the USA'
    #return 'In which city are the headquarters of the United Nations?'
    return 'where was Albert Einstein born'
    #return raw_input("Please enter a question: ")

def load_data(filePath):
    try:
        with open(filePath) as f:
            x = pickle.load(f)
    except:
        x = []
    return x

def save_data(data,filePath):
    with open(filePath, "wb") as f:
        pickle.dump(data, f)

def levenshtein_distance(first, second):
    if len(first) == 0 or len(second) == 0:
        return len(first) + len(second)
    first_length = len(first) + 1
    second_length = len(second) + 1
    distance_matrix = [range(second_length) for i in range(first_length)]
    for i in range(1, first_length):
        for j in range(1, second_length):
            deletion = distance_matrix[i-1][j] + 1
            insertion = distance_matrix[i][j-1] + 1
            substitution = distance_matrix[i-1][j-1]
            if first[i-1] != second[j-1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)
    return distance_matrix[first_length-1][second_length-1]

def calcLeDistance(label,relations):
    minValue = 2
    minString = None
    distance = 100
    label = label.replace(' ','')
    for relation in relations:
        newDist = levenshtein_distance(label.lower(),relation.lower())
        # distance = 10
        # for part in utils.splitCamelCase(relation).split():
        #     newDist = utils.dist_all_synsets(label,part)
        #     if newDist < distance:
        #         distance = newDist
        # newDist = utils.dist_all_synsets(label,relation)
        if newDist < distance:
            distance = newDist
            minString = relation
    minValue = distance
    if distance > 2:
        return "",100
    return minString,minValue

def calcDistance(label,relations):
    minValue = 3
    minString = None
    distance = 100
    label = re.sub('\s','',label)
    for relation in relations:
        # newDist = levenshtein_distance(label,relation)
        distance = 2
        for part in utils.splitCamelCase(relation).split():
            newDist = utils.dist_all_synsets(label,part.lower())
            if newDist < distance:
                distance = newDist

        if distance < minValue:
            minValue = distance
            minString = relation
    # if not distance<0.5:
    #     return "",0.5
    return minString,minValue

def processPatty():
    mat, glove, patty = backend.processPattyData()#glovePath="../glove.6B.50d.txt",pattyPath='yago-relation-paraphrases_json.txt')
    mat, maxLength = backend.padVectors(mat)
    np.asarray(mat).dump('mat.dat')
    np.asarray(maxLength).dump('maxLength.dat')
    # save_data(glove,'glove.dat')
    # save_data(patty,'patty.dat')
    glove = load_data('glove.dat')
    patty = load_data('patty.dat')
    return mat, maxLength, glove, patty

def processQuestion(glove, maxLength, patty, mat,question,dbrs,pa):
    vectors, parts, pos, gen_question, labels, apiResults = frontend.processQuestion(glove,question,minLen=MIN_LENGTH_COMP,maxLen=MAX_LENGTH_COMP,useAPI=USE_TEXT_RAZOR,useSynonyms=False,dps=pa)
    # print (dbrs)
    wdbrs = []
    # for dbr in utils.stripDownExtraWords(dbrs):
    #     for str in dbr.split('_'):
    #         wdbrs.append(str)
    # wparts = []
    # for part in parts:
    #     for dbr in wdbrs:
    #         if part.find(dbr)<0:
    #             wparts.append(part)
    # parts = wparts
    #vectors, _ = backend.padVectors(vectors,maxLength)
    # b = np.ones(proSha[0])
    # a = np.insert(np.array(proVe),50, values = b, axis = 1)
    # similarities = backend.calculateSimilarity(np.array(vectors),proSha[:,:])
    similarities = backend.calculateSimilarity(np.array(vectors),np.array(mat)[:,:-1])
    winnersNum = NUM_WINNERS
    finalCountUnweighted = {}
    finalRelation = {}
    proAr = dict()
    hidproAr = dict()
    proArLin = dict()
    hidproArLin = dict()
    sco = 0
    try:
        jarpath = os.path.join(os.path.abspath('.'), 'entityProperty.jar')
        # print (jpype.isJVMStarted())
        init_jvm(jarpath)
        entityTest = jpype.JClass('entityTest')
        e = entityTest()
        for dbr in dbrs:
            proAr[dbr] = e.getAnnotationProperty(dbr).get("lable")
            proArLin[dbr] = e.getAnnotationProperty(dbr).get("prop")
            hidproAr[dbr] = e.getHiddenProperty(dbr).get("hidLabel")
            hidproArLin[dbr] = e.getHiddenProperty(dbr).get("hidProp")
    except jpype.JavaException, ex:
        print (ex.message())
        # jpype.shutdownJVM()
    for sim in similarities:
        values = list(set(sim))
        #values = np.partition(list(set(sim)),kth=-winnersNum)[-winnersNum:]
        values= [v for v in values if v >= THRESHOLD]
        values = sorted(values,reverse=True)[:winnersNum]
        indexes = []
        for value in values:
            sco = (value-THRESHOLD)*5
            for val in np.where(sim == value)[0]:
                indexes.append(val)
        for index in np.array(indexes).flatten():
            winner = patty.patterns.keys()[int(mat[index][-1])]
            # winner = proAr[dbr][index-1]
            if  finalCountUnweighted.has_key(winner):
                finalCountUnweighted[winner] += sco
                # if finalCountUnweighted[winner]<sco:
                #     finalCountUnweighted[winner] = sco
            else:
                finalCountUnweighted[winner] = 0
                # if  winner in proAr[dbr]:
                #     finalCountUnweighted[winner] += 1
                # else:
                #     finalCountUnweighted[winner] = 1


    finalCountWeighted = finalCountUnweighted.copy()
    # if APPLY_PENILTY:
    #     for relation in finalCountWeighted:
    #         finalCountWeighted[relation] *= patty.weights[relation]
    finalCountWeightedSorted = sorted(finalCountWeighted.items(), key=lambda x:x[1], reverse=True)
    ''' apply the new second iteration '''
    relations = [x[0] for x in finalCountWeightedSorted]
    splittedRelations = utils.splitCamelCase(relations)
    splittedRelations = utils.stripDownExtraWords(splittedRelations)
    newRelations = [utils.makeRelation(r) for r in splittedRelations]
    #splittedRelations = utils.stripDownExtraWords(relations)
    #patternsEmbeddings = [glove.getVector(p) for p in splittedRelations]
    #partsEmbeddings = []
    #finalCountUnweighted = {}
    pro = []
    proLin = []
    hidPro = []
    hidProLin = []
    proRe = []
    proReLin = []
    for dbr in dbrs:
        pro = pro+list(proAr[dbr])
        proLin = proLin+list(proArLin[dbr])
        proRe = proRe+list(proAr[dbr])+list(hidproAr[dbr])
        hidPro = hidPro+list(hidproAr[dbr])
        hidProLin = hidProLin+list(hidproArLin[dbr])
        proReLin = proReLin+list(proArLin[dbr])+list(hidproArLin[dbr])
    # pro = [x for x in pro]
    # proLin = [x for x in proLin]
    # hidPro = [x for x in hidPro]
    # hidProLin = [x for x in hidProLin]
    # proRe = [x for x in proRe]
    # proReLin = [x for x in proReLin]
    str = []
    str1 = []
    for relation in newRelations:
        if relation in [x.lower() for x in pro]:
            if finalCountUnweighted.has_key(relation):
                if not relation in str:
                    str.append(relation)
                    finalCountUnweighted[relation] +=85
                    # if finalCountUnweighted[relation]>0.7:
                    #     finalCountUnweighted[relation] +=110
                    # else:
                    #     finalCountUnweighted[relation] +=70
            else:
                finalCountUnweighted[relation] =85
        else:
            if relation in [x.lower() for x in hidPro]:
                if finalCountUnweighted.has_key(relation):
                    if not relation in str1:
                        str1.append(relation)
                        finalCountUnweighted[relation] +=80
                        # if finalCountUnweighted[relation]>0.7:
                        #     finalCountUnweighted[relation] +=100
                        # else:
                        #     finalCountUnweighted[relation] +=60
                else:
                    finalCountUnweighted[relation] =80
    for part in parts:
        if not len(part) == 0:
            winner,d = calcLeDistance(part, [x for x in proRe])
            if winner:
                if len(winner)>2 and d < 1:
                    if finalCountUnweighted.has_key(winner):
                        finalCountUnweighted[winner]+=150
                    else:
                        finalCountUnweighted[winner]=200
                # else:
                #     if len(winner)>2 and d < 3:
                #         if finalCountUnweighted.has_key(winner):
                #             finalCountUnweighted[winner]+=40
                #         else:
                #             finalCountUnweighted[winner]=60
            winner,d = calcDistance(part, [x for x in proRe])
            if winner:
                if len(winner)>2:
                    if finalCountUnweighted.has_key(winner):
                        finalCountUnweighted[winner]+=40
                    else:
                        finalCountUnweighted[winner]=30
            # if USE_SYNONYMS:
            if True:
                if len(part.split(' ')) == 1:
                    if len(utils.getSynonyms(part))>0:
                        syns = utils.stripDownExtraWords(utils.getSynonyms(part))
                        candidates = []
                        for syn in syns:
                            if not len(syn) == 0:
                                winner = calcDistance(syn, [x for x in proRe])
                                candidates.append(winner)
                        winner = sorted(candidates, key=lambda x:x[1])[0][0]
                        if winner:
                            if len(winner)>2:
                                if finalCountUnweighted.has_key(winner):
                                    finalCountUnweighted[winner]+=40
                                else:
                                    finalCountUnweighted[winner]=30
                else:
                    for pStr in part.split(' '):
                        winner,d = calcLeDistance(pStr, [x for x in proRe])
                        if winner:
                            if len(winner)>2 and d < 1:
                                if finalCountUnweighted.has_key(winner):
                                    finalCountUnweighted[winner]+=100
                                else:
                                    finalCountUnweighted[winner]=100
                            # else:
                            #     if len(winner)>2 and d < 3:
                            #         if finalCountUnweighted.has_key(winner):
                            #             finalCountUnweighted[winner]+=35
                            #         else:
                            #             finalCountUnweighted[winner]=50
                                # winner,d = calcDistance(part, proRe)
                                # print('winner: ', winner)
                                # print (d)
                                # if finalCountUnweighted.has_key(winner):
                                #     finalCountUnweighted[winner]+=10
                                # else:
                                #     finalCountUnweighted[winner]=10
                                # if len(utils.getSynonyms(pStr))>0:
                                #     syns = utils.stripDownExtraWords(utils.getSynonyms(pStr))
                                #     candidates = []
                                #     for syn in syns:
                                #         if not len(syn) == 0:
                                #             winner = calcDistance(syn, proRe)
                                #             candidates.append(winner)
                                #     winner = sorted(candidates, key=lambda x:x[1])[0][0]
                                #     # print ("winner")
                                #     # print (winner)
                                #     if finalCountUnweighted.has_key(winner):
                                #         finalCountUnweighted[winner]+=10
                                #     else:
                                #         finalCountUnweighted[winner]=10
                                #if not len(part) == 0:
                                #    partsEmbeddings.append(glove.getVector(part))
                                #if len(part.split())==1:
                                #    syns = utils.getSynonyms(part)
                                #    for syn in syns[:3]:
                                #        partsEmbeddings.append(glove.getVector(syn))
    #print("=========================================")
    finalCountWeighted = finalCountUnweighted.copy()
    for relation in finalCountWeighted:
        if len(relation)>2:
            if relation in pro:
                # finalRelation[relation] = finalCountWeighted[relation]
                for str in proLin:
                    if str.split('/')[-1]==relation:
                        finalRelation[str] = finalCountWeighted[relation]
            else:
                if relation in hidPro:
                    # finalRelation[relation] = finalCountWeighted[relation]
                    for str in hidProLin:
                        if str.split('/')[-1]==relation:
                            finalRelation[str] = finalCountWeighted[relation]
    # if APPLY_PENILTY:
    #     for relation in finalCountWeighted:
    #         finalCountWeighted[relation] *= patty.weights[relation]
    finalCountWeightedSorted = sorted(finalRelation.items(), key=lambda x:x[1], reverse=True)
    # print (finalCountWeightedSorted)
    ''' end of second iteration '''
    return vectors, parts, pos, gen_question, similarities, finalCountUnweighted, finalRelation, finalCountWeightedSorted, apiResults,proLin,hidProLin

def init_jvm(jarpath = ""):
    if jpype.isJVMStarted():
        return
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-  Xmx4096m", "-Djava.class.path=%s" % jarpath)
# ===== main testing =====          
if __name__ == "__main__":
    mat, maxLength, glove, patty = processPatty()
    #mat=np.load('mat.dat')
    #maxLength=np.load('maxLength.dat')
    #glove = load_data('glove.dat')
    #patty = load_data('patty.dat')
    #patty.processData()
    #vectors, parts, pos, gen_question, similarities, unweighted, weighted, result, _ = processQuestion(glove,maxLength, patty, mat, readQuestion())
