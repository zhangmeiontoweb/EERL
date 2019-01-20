# frontend processing of question

# ===== imports =====
from splitter import Splitter
from tagger import POSTagger
from embedder import Embedder
from pprint import pprint as pp
import types
# import testData
import numpy as np
import textRazorApi as api


# ===== definitions =====
def processQuestion(gloveModel, question, minLen=1,maxLen=3, useAPI=False, useSynonyms=False, dps=[]):
    tagger = POSTagger()
    pos = tagger.parse(question)
    # create splitter and generalizer
    splitter = Splitter()
    if question[-1] == '?' or question[-1] == '.':
        question=question[:-1]
    gen_question = splitter.generalize(question, pos)
    labels = []
    resultsExists = False

    # if len(testData.gparts)==0:
    #     testData.set_gparts()
    parts = []
    for part in dps:
    #     # dp =[]
    #     # for word in part.split(" "):
    #     #    dp.append(' '.join(word))
        parts.append(str(part))
    parts = list(np.array(parts))

    # #start
    # if not useAPI:
    #     parts = list(splitter.split(gen_question,min=minLen,max=maxLen))
    # else:
    #     resultsExists = True
    #     apiResult, _ = api.getBinaryRelations(question)
    #     parts = [rel.predicate for rel in apiResult if len(rel.predicate_positions_) > 1]
    #     for part in parts:
    #         if len(part.split()) > 1:
    #             labels.append(part.split()[0]+''.join(''.join([w[0].upper(), w[1:].lower()]) for w in part.split()[1:]))
    #     if useSynonyms:
    #         predicates = [max(part.split(),key=len) for part in parts]
    #         if predicates is not None and len(predicates) > 0:
    #             for predicate in predicates:
    #                 for part in list(parts):
    #                     if predicate in part:
    #                         for syn in gloveModel.gloveModel.most_similar(predicate.lower()):
    #                             parts.append(part.replace(predicate,syn[0]))
    #     if len(parts) == 0:
    #         resultsExists = False
    #         parts = list(splitter.split(gen_question,min=minLen,max=maxLen))
    # #end

    # create embedder part
    vectors = []


#     part = "ha ha"
#     words = []
#     for word in part.split():
#         words.append(word)
#     vv = list(np.array(words))
#     for a in vv:
#         print ("vvvv1")
#         print (type(a))
#         gloveModel.getVector(a)
    for part in parts:
        vectors.append(gloveModel.getVector(part))
    return vectors, parts, pos, gen_question, labels, resultsExists

# ===== main testing =====          
if __name__ == "__main__":
    pp(processQuestion(Embedder('../glove.6B.50d.txt'),'who was named as president of the USA',useAPI=True,useSynonyms=True))