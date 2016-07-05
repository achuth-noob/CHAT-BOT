import xmltodict
from pattern.en import parse
from pattern.en import pprint
import random
import pickle
import nltk
import nlpnet
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import verbnet as vb
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

list = ["that","on","of","over","with","in","through","over","to","what","how"]

def dependency_parse(input):
    parser = nlpnet.DependencyParser('C:/Users/test/Desktop/NLP/dependency', language='en')
    parsed_text = parser.parse(input)
    sent = parsed_text[0]
    return str(sent.to_conll())

def iden_com_names(input):
    pos = nltk.pos_tag(nltk.word_tokenize(input))
    # print(pos)
    f = open("cab_company_names.txt", 'r')
    comp_names = []
    for i,l in  enumerate(f):
        comp_names.append(l.strip())
    # print(comp_names)
    dep = dependency_parse(input)
    # print(dep)
    dep = dep.split("\n")
    com_name = False
    com_name_sub=False
    com_name_obj = False
    for i in pos:
        if i[1] == "NN" or i[1] == "NNP" or i[1] == "NNS":
            if i[0] in comp_names:
                com_name = True
    if com_name ==1:
        list = []
        for l in dep:
            list.append(l.split())
        for l in range(len(list)):
            if list[l][1] in comp_names:
                if list[l][7]== "SBJ" or list[l+1][7]== "SBJ":
                    com_name_sub = True
                else:
                    com_name_obj =True
    return [com_name,com_name_sub,com_name_obj]

def change_tense(words):
    w = []
    for word in words:
        w.append(WordNetLemmatizer().lemmatize(word,'v'))
    return w

def save_classifier_NBC(classifier):
    f = open('tmp/Verb_classifier.pickle', 'wb')
    pickle.dump(classifier, f, -1)
    f.close()

def load_classifier_NBC(file):
    f = open(file, 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier

def prim_fram(input):
    s = parse(input, relations=True, lemmata=True)
    # print s
    l = parse(input).split()[0]
    m = nltk.pos_tag(input.split(" "))
    # print m
    oy = []
    adj = []
    nph = []
    pph = []
    vbp = []
    adv = []
    exc = []
    for i in range(len(l)):
        tup = (l[i][2],l[i][0])
        oy.append(tup)
    # print oy
    for i in range(len(m)):
        if m[i][1] == "JJ":
            adj.append((m[i][0], i + 1))
    j=0
    x=0
    for i in range(len(oy)-1):
        k = i
        c = i
        np = ""
        vp = ""
        if oy[i][0]=="B-PP":
            pph.append((oy[i][1],i+1))
        if oy[i][0] == "B-ADVP":
            adv.append((oy[i][1], i + 1))
        if oy[i][1] in list:
            # print oy[i][1]
            exc.append((oy[i][1], i + 1))
        if k >=j:

            while(oy[k][0] == "B-NP" or oy[k][0] == "I-NP") and (k <= range(len(oy))):
                np = np + oy[k][1]+" "
                k = k+1
            j = k
            if np!='':
             nph.append((np,j))
        if c >= x:

            while (oy[k][0] == "B-VP" or oy[k][0] == "I-VP") and (k <= range(len(oy))):
                vp = vp + oy[k][1] + " "
                k = k + 1
            x = k
            if vp != '':
                vbp.append((vp, j))

    # print vbp
    sen = nph+pph+vbp+adv+exc+adj
    # print sen
    sen1 = sorted(sen, key=lambda x: x[1])
    # print sen1
    senf = []
    for i in range(len(sen1)-1):
        u = sen1[i + 1]
        if sen1[i][0] != u[0]:
            senf.append(sen1[i])
    senf.append(sen1[-1])
    # print senf
    frame = []
    for z in range(len(senf)):
        if (senf[z] in nph):
            if(z>=2 and "ing" in senf[z][0]):
                frame.append((senf[z][0],"ING"))
                continue
            frame.append((senf[z][0], "NP"))
            continue
        if senf[z] in pph:
            if (z>2 and "ing" in senf[z][0]):
                frame.append((senf[z][0], "ING"))
                continue
            frame.append((senf[z][0], "PP"))
            continue
        if senf[z] in exc:
            frame.append((senf[z][0], senf[z][0]))
            continue
        if senf[z] in vbp:
            if (z>=2 and "ing" in senf[z][0]):
                frame.append((senf[z][0], "ING"))
                continue
            frame.append((senf[z][0], "VP"))
            continue
        if senf[z] in adv:
            if (z>2 and "ing" in senf[z][0]):
                frame.append((senf[z][0], senf[z][0]))
                continue
            frame.append((senf[z][0], "ADVP"))
            continue

        if senf[z] in adj:
            if (z>2 and "ing" in senf[z][0]):
                frame.append((senf[z][0], senf[z][0]))
                continue
            frame.append((senf[z][0], "ADJ"))
            continue
    vbf = []

    ps = PorterStemmer()
    for i in vbp:
        h = vb.classids(ps.stem(i[0].lower().strip()))
        # print h
        if h != []:
             vbf.append(ps.stem(i[0].strip()))

    return vbf,frame


# v,k = prim_fram("will you please book me a ride ?")
# dog = wordnet.synset('drive.v.01')
# cat = wordnet.synset('ride.v.01')
# print(v)
# print(k)
# from nltk.corpus import wordnet_ic
# print(wordnet.synsets('king'))
# print(wordnet.synsets('queen'))
# print(wordnet.path_similarity(dog,cat))
# print(dog.wup_similarity(cat))
# semcor_ic = wordnet_ic.ic('ic-semcor.dat')
# print(dog.lin_similarity(cat, semcor_ic))
# for i in wordnet.synsets(''):
#     for j in wordnet.synsets('queen'):
#         # print(wordnet.path_similarity(i, j, simulate_root=False))
#         k=k+1
#         # print(k)
#         try:
#             l=l+
#         except:
#             continue

# dog = wordnet.synset('dog.n.01')
# hyper = lambda s: s.hypernyms()
# print(dog.closure(hyper))

# g = l/k
# print(g)
#---------------------------------------------training---------------------------------------------
# f = open("features_verbs.txt","r")
# q = open("dataset_request_verbs.txt","r")
# fg = open("dataset_non-request_verbs.txt","r")
#
# # word_features = []
# #
# # for l,i in enumerate(f):
# #     word_features.append(i)
# # f.close()
# #
# featuresset = []
# # def find_features(document):
# #     words = set(document)
# #     features = {}
# #     for w in word_features:
# #         features[w] = (w in words)
# #     # print(features)
# #     return features
#
# for t,op in enumerate(q):
#     verblist,frames_list = prim_fram(op)
#     # print(verblist)
#     verblist = change_tense(verblist)
#     for r in range(len(verblist)):
#         keys = []
#         ids = vb.classids(verblist[r])
#         for i in ids:
#             u = vb.vnclass(i)
#             for j in [l.attrib['type'] for l in u.findall('THEMROLES/THEMROLE/SELRESTRS/SELRESTR')]:
#                 keys.append(j)
#             for j in [l.attrib['type'] for l in u.findall('THEMROLES/THEMROLE')]:
#                 keys.append(j)
#             for j in [l.attrib['value'] for l in u.findall('FRAMES/FRAME/SEMANTICS/PRED')]:
#                 keys.append(j)
#             # print(keys)
#         f = open("features_verbs.txt", "r")
#         word_features = []
#
#         for l, i in enumerate(f):
#             word_features.append(i.strip("\n"))
#         f.close()
#
#         def find_features(document,input):
#             words = set(document)
#             features = {}
#             for w in word_features:
#                 features[w] = (w in words)
#             # print(features)
#             [features["com_name"], features["com_name_sbj"], features["com_name_obj"]] = iden_com_names(input)
#             return features
#         featuresset.append((find_features(keys,op),"Requesting_Cab_Service"))
# # for i in featuresset:
# #     print(i)
# # print type(r)
#
# ghhf = []
# for g,p in enumerate(fg):
#     vlist, flist = prim_fram(p)
#     # print(vlist)
#     vlist = change_tense(vlist)
#     for r in range(len(vlist)):
#         keys = []
#         ids = vb.classids(vlist[r])
#         for i in ids:
#             u = vb.vnclass(i)
#             for j in [l.attrib['type'] for l in u.findall('THEMROLES/THEMROLE/SELRESTRS/SELRESTR')]:
#                 keys.append(j)
#             for j in [l.attrib['type'] for l in u.findall('THEMROLES/THEMROLE')]:
#                 keys.append(j)
#             for j in [l.attrib['value'] for l in u.findall('FRAMES/FRAME/SEMANTICS/PRED')]:
#                 keys.append(j)
#         print(keys)
#         f = open("features_verbs.txt", "r")
#         word_features = []
#         # word_features = word_features+["com_name","com_name_sbj","com_name_obj"]
#
#         for l, i in enumerate(f):
#             word_features.append(i.strip("\n"))
#         f.close()
#
#         def find_features(document,input):
#             words = set(document)
#             features = {}
#             for w in word_features:
#                 features[w] = (w in words)
#             [features["com_name"],features["com_name_sbj"],features["com_name_obj"]] = iden_com_names(input)
#             # print(features)
#             return features
#         featuresset.append((find_features(keys,p),"Not_Requesting_Cab_service"))
#         ghhf.append((find_features(keys,p),"Not_Requesting_Cab_service"))
#         # print(featuresset,g)
# for i in ghhf:
#     print(i)
# # for i in featuresset:
# #     print(i)
# random.shuffle(featuresset)
# classifier = nltk.NaiveBayesClassifier.train(featuresset)
# save_classifier_NBC(classifier)

#-----------------------------------------testing---------------------------------------------------
input = "He need a ride from his home."
verb_list, frames_list = prim_fram(input)
print(frames_list)
print(nltk.pos_tag(nltk.word_tokenize(input)))
print(verb_list)
for r in range(len(verb_list)):
    keys = []
    ids = vb.classids(verb_list[r])
    for i in ids:
        u = vb.vnclass(i)
        for j in [l.attrib['type'] for l in u.findall('THEMROLES/THEMROLE/SELRESTRS/SELRESTR')]:
            keys.append(j)
        for j in [l.attrib['type'] for l in u.findall('THEMROLES/THEMROLE')]:
            keys.append(j)
        for j in [l.attrib['value'] for l in u.findall('FRAMES/FRAME/SEMANTICS/PRED')]:
            keys.append(j)
    f = open("tmp/features_verbs.txt","r")
    word_features = []

    for l,i in enumerate(f):
        word_features.append(i)
    f.close()

    def find_features(document, input):
        words = set(document)
        features = {}
        for w in word_features:
            features[w] = (w in words)
        [features["com_name"], features["com_name_sbj"], features["com_name_obj"]] = iden_com_names(input)
        # print(features)
        return features
    print(keys)
    print(load_classifier_NBC("tmp/Verb_classifier.pickle").classify(find_features(keys,input)))