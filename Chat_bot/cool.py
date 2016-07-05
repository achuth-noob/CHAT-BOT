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

def is_country(keyword):
    keys = query(keyword)
    if "country" in keys or "place" in keys:
        return True
    return False

def query(input):
    keyword = []
    stop_words = set(stopwords.words("english"))
    dic = [".", ",", "(", ")", "{", "}", "'ve", "is", "am", "are", "of", "and", "from", "for", "the", "to", "--", ";", ":", "..."]
    try:
        r = requests.get("http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryString="+input)
        root = ET.fromstring(remove_non_ascii(r.text))
        # print(r.text)
        keywords = []
        for i in range(len(root)):
            for j in range(8):
                if root[i][0].find(input)==-1:
                    break
                if j==3:
                    for k in range(len(root[i][j])):
                        for l in root[i][j][k][0].text.split(" "):
                            if l not in stop_words:
                                if l not in dic:
                                    if l.find("http")==-1:
                                        keywords.append(l)
                if j==4:
                    for k in range(len(root[i][j])):
                        for l in root[i][j][k][0].text.split(" "):
                            if l not in stop_words:
                                if l not in dic:
                                    if l.find("http") == -1:
                                        keywords.append(l)
        keywords = POS_tagging(keywords)
        l = []
        for i in keywords:
            if i[1] != "CD" and i[0] not in dic and len(i[0]) > 2:
                l.append(i[0])
        keyword = l
    except:
        # print("query has no data in our database")
        return keyword
    print(keyword)
    return keyword

def POS_tagging(corpus):
    train_text = state_union.raw("2005-GWBush.txt")
    sample_text = ""
    for i in corpus:
        sample_text = sample_text+i+" "
    tuples_list = []
    def process_content():
        try:
            words = nltk.word_tokenize(sample_text)
            tagged = nltk.pos_tag(words)
            for w in tagged:
                tuples_list.append(w)
        except Exception as e:
            print(str(e))
    process_content()
    return tuples_list
    # textfile.close()

list = ["that","on","of","over","with","in","through","over","to","what","how"]
dic = [".", ",", "#", "(", ")", "{", "}", "'ve", "is", "am", "are", "of", "and", "from", "for", "the", "to", "--", ";", ":", "..."]

def remove_non_ascii(corpus):
    str=""
    for i in corpus:
        if 32<=ord(i)<=122:
            str=str+i
    return str

def save_classifier_NBC(classifier):
   f = open('NBC_Categorization1.pickle', 'wb')
   pickle.dump(classifier, f, -1)
   f.close()

def load_classifier_NBC(file):
   f = open(file, 'rb')
   classifier = pickle.load(f)
   f.close()
   return classifier

def dependency_parse(input):
    parser = nlpnet.DependencyParser('C:/Users/test/Desktop/NLP/dependency', language='en')
    parsed_text = parser.parse(input)
    sent = parsed_text[0]
    return str(sent.to_conll())

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

def sorting(fil_addr,cre_addr):
    fil_addr = "D:/Data_NLP/Bag_of_words_data/"+fil_addr
    fi = open(fil_addr,'r')
    con = []
    for l,i in enumerate(fi):
        con.append(i.strip("\n"))
    con.sort()
    cre_addr = "D:/Data_NLP/Bag_of_words_data/"+cre_addr
    f = open(cre_addr,'a')
    for item in set(con):
        f.write(item)
        f.write("\n")
    f.close()

def binary_search(lis,keyword):
    flag = False
    start = 0
    end = len(lis)
    while(start<end):
        mid = (start+end)//2
        if lis[mid] < keyword:
            # print(lis[mid], keyword,'<')
            start = mid + 1
        elif lis[mid] > keyword:
            # print(lis[mid], keyword, '>')
            end = mid-1
        else:
            # print(lis[mid], keyword, '==')
            flag = True
            break
    return flag

def found(fil_addr,key_word):
    fil_addr = "D:/Data_NLP/Bag_of_words_data/"+fil_addr
    fi = open(fil_addr,'r')
    cop = []
    for hj,i in enumerate(fi):
        cop.append(i.strip("\n").lower())
    # print(key_word,"sdjgh")
    fi.close()
    l = False
    # l = binary_search(cop,key_word)
    if key_word.lower() in cop:
        l= True
    if l != False:
        return True
    else:
        return False

def categ(keyword):
    lis = []
    if found("Movies__sorted.txt",keyword.lower()) == True:
        lis.append("Movies")
    if found("Sport__sorted.txt", keyword.lower()) == True:
        lis.append("Sports")
    if found("Gadgets__sorted.txt", keyword.lower()) == True:
        lis.append("Gadgets")
    if found("Automobiles__sorted.txt", keyword.lower()) == True:
        lis.append("Automobiles")
    if found("Politics__sorted.txt", keyword.lower()) == True:
        lis.append("Politics")
    if lis == []:
        lis.append("Nothing Found")
    return lis

v = open("features_all.txt","r")
word_features = []
for l,i in enumerate(v):
    word_features.append(i.strip("\n"))
v.close()

def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    # print(features)
    return features


#Messi nutmeg on the keeper had check level x99999999.
#Gujarat CM Anandiben Patel faced protest by Patidar women at Hardik Patel's hometown Viramgam.
#Chief minister Pinarayi Vijayan confirms the arrest of Assam native who killed Jisha in Perumbavur
#Police put Patidar reservation stir leader Hardik Patel's family under house arrest due to CM's program in Viramgam.
#I have left behind many of my dreams to achieve this Olympics gold.
#Yuzi's 2-25 & Rahul's 63* helped India seal the whitewash with a 10 wicket win!
#They take out Lukaku and more goals come in.
#Ronaldo's performance is very poor today.
#The rating of the Hyundai i10 is quite good.
#What's the review of the movie Batman vs Superman???
#India batting first...... Rohit Sharma and Rahane opening.
#Want to Dhoni batting in Pune..miss u dhoni in yellow jersey... IPL fever begins
#What is the review of Amazing Spiderman 2?
#Sun risers Hyderabad won the match against Gujarat Lions with 10 wickets..... Wat a match
#Csn anyone tell the best website to buy Samsung Galaxy s7.
#I just bought a new Logitech keyboard it works well.
#It is a very good experience to drive in Mercedes.
#Mumbai Indians have to score 175 in 20 overs to win against Kolkata Knight Riders..... Watching Rohit Sharma batting is soothing my eyes.....:-):-)
#BlackBerry planning to launch two new mid-range Android smartphones.
#Sennheiser looks to set up stores in India.
#Uber expands to more cities in China
#iOS 10 has smarter Siri, revamped Photos app, iMessages and more


input = "Where can I get a ride?"

pos = nltk.pos_tag(nltk.word_tokenize(input))
nouns = []
adjectives = []
verbs = []
for i in pos:
    if "NN" in i[1]:
        nouns.append(i[0])
    if "JJ" in i[1]:
        adjectives.append(i[0])
    if "VB" in i[1]:
        verbs.append(i[0])
print("Nouns ",nouns)
print("Adjectives ",adjectives)
print("Verbs ",verbs)
a,s,d,f,g,h,j = imp_parsing(input)
print("NP_person_list ",a)
print("NP_organization_list ",s)
print("NP_important_list ",d)
print("np_list ",f)
m = []
n = []
o = []
country = []
for i in g:
    if is_country(i)==True:
        country.append(i)
    else:
        m.append(i)

for i in h:
    if is_country(i):
        country.append(i)
    else:
        n.append(i)
for i in f:
    if is_country(i):
        country.append(i)
    else:
        o.append(i)
print("persons_list",m)
print("country_list",country)
print("organization_list ",n)
print("important_list ",o)
print("\n")
print("identifying Persons.....")
if g == []:
    print("General")
else:
    for i in m:
        if query(i) != []:
            print(load_classifier_NBC("NBC_Categorization1.pickle").classify(find_features(query(i))))
        else:
            print("General")
print("\n")
print("Identifying Organizations.....")
if h == []:
    print("General")
else:
    for i in n:
        if query(i) != []:
            print(load_classifier_NBC("NBC_Categorization1.pickle").classify(find_features(query(i))))
        else:
            print("General")
print("\n")
print("Identifying Important entities.....")
if j == []:
    print("General")
else:
    for i in o:
        if query(i) != []:
            print(load_classifier_NBC("NBC_Categorization1.pickle").classify(find_features(query(i))))
        else:
            print("General")
print("\n")
print("Checking noun terms in bag of words.....")
noun_categ = []
for i in nouns:
    noun_categ.append(j for j in categ(i))
    print(i,categ(i))
print("\n")
print("Checking adjectives terms in bag of words.....")
adj_categ = []
for i in adjectives:
    adj_categ.append(j for j in categ(i))
    print(i,categ(i))
if adj_categ == []:
    print("Nothing found")
print("\n")
print("Checking verb terms in bag of words.....")
verb_categ = []
for i in verbs:
    verb_categ.append(j for j in categ(i))
    print(i,categ(i))

print(dependency_parse(input))