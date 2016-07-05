import nlpnet
import nltk
import xmltodict
from pattern.en import parse
from pattern.en import pprint
import random
import pickle
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import verbnet as vb
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import wordnet
from nltk.corpus import state_union
from nltk.stem.wordnet import WordNetLemmatizer


list = ["that","on","of","over","with","in","through","over","to","what","how"]

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

def remove_non_ascii(corpus):
    str=""
    for i in corpus:
        if 32<=ord(i)<=122:
            str=str+i
    return str

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
    except Exception as e:
        print(str(e))
    return namedEnt

def dependency_parse(input):
    parser = nlpnet.DependencyParser('C:/Users/test/Desktop/NLP/dependency', language='en')
    parsed_text = parser.parse(input)
    sent = parsed_text[0]
    return str(sent.to_conll())

def imp_parsing(input):
    st ,fr= prim_fram(input)
    l = name_ent_recog(input)
    np_list=[]
    for i in fr:
        if i[1] == 'NP':
            np_list.append(i[0])
    persons = []
    organizations = []
    important = []
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
                np_persons_list.append(i)
        for j in organizations:
            if j in i:
                np_organizationa_list.append(i)
        for j in important:
            if j in i:
                np_important_list.append(i)
    vf = []
    for i in np_list:
        if i not in np_persons_list and i not in np_organizationa_list and i not in np_important_list:
            vf.append(i)
    return np_persons_list,np_organizationa_list,np_important_list,vf

#i hav lft behind many f my dreams to achieve this Olympic Gold.
#Police put Patidar reservation stir leader Hardik Patel's family under house arrest due to CM's program in Viramgam.
#Chief minister Pinarayi Vijayan confirms the arrest of Assam native who killed Jisha in Perumbavur.
#Yuzi's 2-25 & Rahul's 63* helped India seal the whitewash with a 10 wicket win!

input = "Yuzi's 2-25 & Rahul's 63* helped India seal the whitewash with a 10 wicket win!"
a,s,d,f = imp_parsing(input)
print(a)
print(s)
print(d)
print(f)
