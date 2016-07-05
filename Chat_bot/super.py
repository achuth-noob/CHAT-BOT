import os
import re
import nltk
import gensim
import random
import pickle
import nlpnet
import requests
import xmltodict
import wikipedia
from pattern.en import parse
from pattern.en import pprint
from bisect import bisect_left
from nltk.corpus import wordnet
from nltk.corpus import stopwords
import xml.etree.ElementTree as ET
from nltk.stem import PorterStemmer
from nltk.corpus import state_union
from nltk.corpus import verbnet as vb
from nltk.tokenize import word_tokenize
from nltk import PunktSentenceTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import verbnet as vbnet

list = ["that","on","of","over","with","in","through","over","to","what","how"]

def imp_parsing(input):
    st ,fr= prim_fram(input)
    l = name_ent_recog(input)
    print(l)
    np_list=[]
    for i in fr:
        if i[1] == 'NP':
            np_list.append(i[0])
    persons = []
    organizations = []
    important = []
    countries = []
    for i in l[0]:
        if str(i).find("PERSON")!=-1:
            i = str(i).strip("(PERSON").strip(")")
            string = ""
            i = i.split()
            for j in i:
                string = string + j.split("/")[0] + " "
            print(string)
            persons.append(string.strip())
        if str(i).find("ORGANIZATION")!=-1:
            i = str(i).strip("(ORGANIZATION").strip(")")
            string = ""
            i = i.split()
            for j in i:
                string = string + j.split("/")[0] + " "
            print(string)
            organizations.append(string.strip())
        if str(i).find("GPE") != -1:
            i = str(i).strip("(GPE").strip(")")
            string = ""
            i = i.split()
            for j in i:
                string = string + j.split("/")[0] + " "
            print(string)
            important.append(string.strip())
    np_persons_list = []
    np_organizationa_list = []
    np_important_list = []
    for i in np_list:
        for j in persons:
            if j in i:
                np_persons_list.append(i.strip())
        for j in organizations:
            if j in i:
                np_organizationa_list.append(i.strip())
        for j in important:
            if j in i:
                np_important_list.append(i.strip())
    vf = []
    for i in np_list:
        if i not in np_persons_list and i not in np_organizationa_list and i not in np_important_list:
            vf.append(i)
    return np_persons_list,np_organizationa_list,np_important_list,vf,persons,organizations,important

def name_ent_recog(post):
    train_text = state_union.raw("2005-GWBush.txt")
    sample_text = post
    custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
    tokenized = custom_sent_tokenizer.tokenize(sample_text)
    namedEnt = []
    try:
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            namedEnt.append(nltk.ne_chunk(tagged))
            # chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP.?>*<NN>?}"""
            # # chunkGram = r"""Chunk: {<.*>+}
            # #                     }<VB.?|IN|DT>+{"""
            # chunkParser = nltk.RegexpParser(chunkGram)
            # chunked = chunkParser.parse(tagged)
            # print(chunked)
            # #print(tagged)
    except Exception as e:
        print(str(e))
    return namedEnt

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

def dependency_parse(input):
    parser = nlpnet.DependencyParser('C:/Users/test/Desktop/NLP/dependency', language='en')
    parsed_text = parser.parse(input)
    sent = parsed_text[0]
    return str(sent.to_conll())

def change_tense(words):
    w = WordNetLemmatizer().lemmatize(words,'v')
    return w

def is_req_verb(keyword):
    thematic_roles = []
    selres = []
    semantics = []
    themroles_dict = {}
    semantics_dict = {}
    selres_dict = {}
    flag = False
    requesting_verbs = 0
    l = vbnet.classids(keyword)
    if l!=[]:
        for i in l:
            t=2
            s = str(vbnet.pprint(i))
            # print(s)
            subclasses = s.split("Subclasses:")[1].split("Members:")[0].strip()
            theme = s.split("Thematic roles:")[1].split("Frames")[0]
            seman = s.split("Semantics:")[1:]
            for j in seman:
                k = j.split("\n")
                for w in k:
                    if '*' in w:
                        if w.strip("        * ").split("(")[0] in semantics_dict:
                            semantics.append(w.strip("        * ").split("(")[0].strip())
                            continue
                        else:
                            semantics.append(w.strip("        * ").split("(")[0].strip())
                            semantics_dict[w.strip("        * ").strip()] = 1
            for j in theme.split("\n"):
                if j != '' and j != '  ':
                    if j.strip("   *").find('[') != -1:
                        # print(i.strip("   *"))
                        if j.strip("   *").split('[')[0] in themroles_dict:
                            thematic_roles.append(j.strip("   *").split('[')[0].strip())
                            continue
                        else:
                            thematic_roles.append(j.strip("   *").split('[')[0].strip())
                            themroles_dict[j.strip("   *").split('[')[0].strip()] = 1
                        for k in j.strip("   *").split('[')[1].split(']')[0].split('+'):
                            if k != "":
                                if k in selres_dict:
                                    selres.append(k.strip())
                                    continue
                                else:
                                    selres.append(k.strip())
                                    selres_dict[k.strip()] = 1
                    elif j.strip("   *").find('[') == -1:
                        if j.strip("   *") in themroles_dict:
                            thematic_roles.append(j.strip("   *").strip())
                            continue
                        else:
                            thematic_roles.append(j.strip("   *").strip())
                            themroles_dict[j.strip("   *").strip()] = 1

            while(subclasses!="(none)"):
                s = str(vbnet.pprint(subclasses.split(" ")[0]))
                subclasses = s.split("Subclasses:")[1].split("Members")[0].strip()
                theme = s.split("Thematic roles:")[1].split("Frames")[0]
                seman = s.split("Semantics:")[1:]
                for j in seman:
                    k = j.split("\n")
                    for w in k:
                        if '*' in w:
                            if w.strip("        * ").split("(")[0] in semantics_dict:
                                semantics.append(w.strip("        * ").split("(")[0].strip())
                                continue
                            else:
                                semantics.append(w.strip("        * ").split("(")[0].strip())
                                semantics_dict[w.strip("        * ").strip()] = 1
                for j in theme.split("\n"):
                    if j != '' and j != '  ':
                        if j.strip("   *").find('[') != -1:
                            # print(i.strip("   *"))
                            if j.strip("   *").split('[')[0] in themroles_dict:
                                thematic_roles.append(j.strip("   *").split('[')[0].strip())
                                continue
                            else:
                                thematic_roles.append(j.strip("   *").split('[')[0].strip())
                                themroles_dict[j.strip("   *").split('[')[0].strip()] = 1
                            for k in j.strip("   *").split('[')[1].split(']')[0].split('+'):
                                if k != "":
                                    if k in selres_dict:
                                        selres.append(k.strip())
                                        continue
                                    else:
                                        selres.append(k.strip())
                                        selres_dict[k.strip()] = 1
                        elif j.strip("   *").find('[') == -1:
                            if j.strip("   *") in themroles_dict:
                                thematic_roles.append(j.strip("   *").strip())
                                continue
                            else:
                                thematic_roles.append(j.strip("   *").strip())
                                themroles_dict[j.strip("   *").strip()] = 1

    # print("thematic_roles",set(thematic_roles))
    # print("selectional restrictors",set(selres))
    # print("semantics",set(semantics))
    if "desire" in semantics or "command" in semantics or "direction" in semantics or "motion" in semantics or "location" in semantics or "has_possession" in semantics:
        flag = True
    if flag == True:
        requesting_verbs = 1
    return requesting_verbs

input = "Book me a pizza."
# a,s,d,f,g,h,j = imp_parsing(input)
pos = nltk.pos_tag(nltk.word_tokenize(input))
# print(pos)
verbs = []
for i in pos:
    if "VB" in i[1]:
        verbs.append(change_tense(i[0].lower()))

# print(dependency_parse(input))
lw=dependency_parse(input).split("\n")

rootpos = "-1"
objpos = "-1"
objpoint = "-1"
vc = "-1"

for i in range(len(lw)):
    lw[i] = lw[i].split()

flag = False
fg = open("services_keywords.txt","r")
ls = []
for l,i in enumerate(fg):
    ls.append(i.strip("\n").strip())

for hg in verbs:
    r = is_req_verb(hg.strip())
    if r==1:
        for i in lw:
            if i[1].lower().strip()==hg:
                if i[7].strip() == "ROOT" :
                    rootpos = i[0].strip()
                if i[7].strip() == "VC":
                    vc = i[0].strip()
            if i[7].strip() == "OBJ" and i[1].lower().strip() in ls:
                if i[6].lower().strip() == vc or i[6].lower().strip() == rootpos:
                    flag = True
print(flag)