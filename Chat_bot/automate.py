import requests
import gensim
import nltk
import pickle
import wikipedia
import nlpnet
import random
from nltk import PunktSentenceTokenizer
from nltk.corpus import state_union
import xml.etree.ElementTree as ET
from nltk.corpus import stopwords
import xmltodict
from pattern.en import parse
from pattern.en import pprint
import pickle
import nlpnet
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import verbnet as vb
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

list = ["that","on","of","over","with","in","through","over","to","what","how"]
dic = [".", ",", "#", "(", ")", "{", "}", "'ve", "is", "am", "are", "of", "and", "from", "for", "the", "to", "--", ";", ":", "..."]

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

def decide_features(add,num):
    f = open(add, "r")
    list = []
    for l,i in enumerate(f):
        list.append(i)
    lise = POS_tagging(list)
    l = []
    for i in lise:
        if i[1]!="CD" and i[0] not in dic and len(i[0])>2:
            l.append(i[0])
    lis = nltk.FreqDist(l)
    list = lis.most_common(num)
    j =[]
    for i in list:
        j.append(i[0])
    return j

def run(add,num):
    f = open(add,"r")
    features_Movies = []
    features_Gadgets = []
    features_Automobiles = []
    features_Sports = []
    features_Politics = []
    features = []
    for l,i in enumerate(f):
        category = i.strip("all_words_")
        category = category.strip("\n")
        category = category.strip(".txt")
        print(category)
        if category == "Movies":
            for j in decide_features(i.strip("\n"),num):
                features_Movies.append(j)
                features.append(j)
        if category == "Automobiles":
            for j in decide_features(i.strip("\n"), num):
                features_Automobiles.append(j)
                features.append(j)
        if category == "Politics":
            for j in decide_features(i.strip("\n"), num):
                features_Politics.append(j)
                features.append(j)
        if category == "Gadgets":
            for j in decide_features(i.strip("\n"), num):
                features_Gadgets.append(j)
                features.append(j)
        if category == "Sports":
            for j in decide_features(i.strip("\n"), num):
                features_Sports.append(j)
                features.append(j)
    return features_Sports,features_Gadgets,features_Politics,features_Automobiles,features_Movies,features

def add_acc(tuple):
    f = open("accuracycheck_keyword.txt","a")
    m = open("accuracycheck_category.txt","a")
    f.write(tuple[0])
    f.write("\n")
    m.write(tuple[1])
    m.write("\n")

def remove_non_ascii(corpus):
    str=""
    for i in corpus:
        if 32<=ord(i)<=122:
            str=str+i
    return str

def entity_similarity(keyword):
    model = gensim.models.Word2Vec.load("D:\Data_NLP\wiki.en.text1.model")
    list = model.most_similar(keyword)
    print(list)
    # print(wikipedia.summary(keyword))
    print("\n")
    summary_list=[]
    try:
        for i in list:
            try:
                c=0
                # summary_list.append(wikipedia.summary(i[0]))
            except:
                continue
    except Exception as e:
        print(e)

def save_classifier_NBC(classifier):
   f = open('NBC_Categorization1.pickle', 'wb')
   pickle.dump(classifier, f, -1)
   f.close()

def load_classifier_NBC(file):
   f = open(file, 'rb')
   classifier = pickle.load(f)
   f.close()
   return classifier

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

def dependency_parse(input):
    parser = nlpnet.DependencyParser('C:/Users/test/Desktop/NLP/dependency', language='en')
    parsed_text = parser.parse(input)
    sent = parsed_text[0]
    return str(sent.to_conll())

# print(dependency_parse("He adapted himself to waking up early."))

def label_data(add, category):
    f = open(add, "r")
    data = []
    for l,i in enumerate(f):
        if query(input) != None:
            data.append((query(i) , category))
    return data

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


#--------------------------------Scrape and save data---------------------------
# f = open("gadgets.txt","r")
# for i,l in enumerate(f):
#     print(l)
#     fe = open("all_words_gadgets.txt", "a")
#     for j in query(l):
#         try:
#             fe.write(str(j))
#             fe.write("\n")
#         except:
#             continue
#     fe.close()
# # entity_similarity("Saumitra Khan")
#---------------------------------------------------------------------------------

# features_Sports,features_Gadgets,features_Politics,features_Automobiles,features_Movies,word_features = run("temp_classification.txt", 500)
# n = open("features_all.txt","a")
# word_features = set(word_features)
# for i in word_features:
#     n.write(str(i))
#     n.write("\n")
# n.close()
# n = open("features_Sports.txt","a")
# for i in features_Sports:
#     n.write(str(i))
#     n.write("\n")
# n.close()
# n = open("features_Gadgets.txt","a")
# for i in features_Gadgets:
#     n.write(str(i))
#     n.write("\n")
# n.close()
# n = open("features_Politics.txt","a")
# for i in features_Politics:
#     n.write(str(i))
#     n.write("\n")
# n.close()
# n = open("features_Automobiles.txt","a")
# for i in features_Automobiles:
#     n.write(str(i))
#     n.write("\n")
# n.close()
# n = open("features_Movies.txt","a")
# for i in features_Movies:
#     n.write(str(i))
#     n.write("\n")
# n.close()

#------------------------------------------------------------------------------------

v = open("features_all.txt","r")
word_features = []
for l,i in enumerate(v):
    word_features.append(i.strip("\n"))
v.close()
# v = open("features_Politics.txt","r")
# features_Politics = []
# for l,i in enumerate(v):
#     features_Politics.append(i.strip("\n"))
# v.close()
# v = open("features_Movies.txt","r")
# features_Movies = []
# for l,i in enumerate(v):
#     features_Movies.append(i.strip("\n"))
# v.close()
# v = open("features_Sports.txt","r")
# features_Sports = []
# for l,i in enumerate(v):
#     features_Sports.append(i.strip("\n"))
# v.close()
# v = open("features_Automobiles.txt","r")
# features_Automobiles = []
# for l,i in enumerate(v):
#     features_Automobiles.append(i.strip("\n"))
# v.close()
# v = open("features_Gadgets.txt","r")
# features_Gadgets = []
# for l,i in enumerate(v):
#     features_Gadgets.append(i.strip("\n"))
# v.close()


# word_features = set(word_features)
# print(word_features)
# m = open("total_data.txt","a")

#-----------------------this function is for training---------------------------
# def find_features_categ(document,features_categ):
#     words = set(document)
#     features = {}
#     for w in features_categ:
#         features[w] = (w in words)
#     list = []
#     for key in features.iterkeys():
#         if features[key] == True:
#             list.append(key)
#     feature = {}
#     for key in word_features:
#         feature[key] = False
#     for i in list:
#         feature[i]=True
#     # print(features)
#     return feature

#-----------------------this function is for testing---------------------------
def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    # print(features)
    return features

# featuresets = []
# politics = label_data("politics.txt", "Politics")
# for rev,category in politics:
#     featuresets.append((find_features_categ(rev,features_Politics),category))
#
# Automobiles = label_data("motorcycle_manufacturers.txt", "Automobiles")
# for rev,category in Automobiles:
#     featuresets.append((find_features_categ(rev,features_Automobiles),category))
#
# Movies = label_data("Movies_queries.txt", "Movies")
# for rev,category in Movies:
#     featuresets.append((find_features_categ(rev,features_Movies),category))
#
# Sports = label_data("Sports_queries.txt","Sports")
# for rev,category in Sports:
#     featuresets.append((find_features_categ(rev,features_Sports),category))
#
# Gadgets = label_data("gadgets.txt","Gadgets")
# for rev,category in Gadgets:
#     featuresets.append((find_features_categ(rev,features_Gadgets),category))
# random.shuffle(featuresets)

# for i in tot_tup_list:
#     m.write(str(i))
# m.close()

# training_set = featuresets[:3500]
# testing_set = featuresets[3500:]
# classifier = nltk.NaiveBayesClassifier.train(training_set)
# save_classifier_NBC(classifier)
# print("Naive Bayes Algo accuracy:", (nltk.classify.accuracy(load_classifier_NBC("NBC_Categorization.pickle"),testing_set))*100)


# print(load_classifier_NBC("NBC_Categorization.pickle").classify(find_features(query(input))))
# print(query("Lenovo"))
# print(entity_similarity(""))
#-----------------------------------------------------------------------------------------------------------------------
# count = 0
# n = 0
# f = open("accuracycheck_category.txt","r")
# g = open("accuracycheck_keyword.txt","r")
# for l,i in enumerate(f):
#     if load_classifier_NBC("NBC_Categorization.pickle").classify(find_features(query(g.readline(l).strip("\n")))) == i.strip("\n"):
#         count = count+1
#     # print(load_classifier_NBC("NBC_Categorization.pickle").classify(find_features(query(g.readline(l)))))
#     n = n+1
# print(count/n)





#That Messi nutmeg on the keeper had check level x99999999
#Gujarat CM Anandiben Patel faced protest by Patidar women at Hardik Patel's hometown Viramgam.
#Chief minister Pinarayi Vijayan confirms the arrest of Assam native who killed Jisha in Perumbavur
#Police put Patidar reservation stir leader Hardik Patel's family under house arrest due to CM's program in Viramgam.
#I have left behind many of my dreams to achieve this Olympics gold.
#Yuzi's 2-25 & Rahul's 63* helped India seal the whitewash with a 10 wicket win!
#They take out Lukaku and more goals come in.
#Ronaldo's performance is very poor today
#The rating of the Hyundai i10 is quite good.
#What's the review of the movie Batman vs Superman???
#India batting first...... Rohit Sharma and Rahane opening
#Want to Dhoni batting in Pune..miss u dhoni in yellow jersey... IPL fever begins
#What is the review of Amazing Spiderman 2?
#Sun risers Hyderabad won the match against Gujarat Lions with 10 wickets..... Wat a match
#Csn anyone tell the best website to buy Samsung Galaxy s7.
#I just bought a new logitech keyboard it works well.
#It is a very good experience to drive in Mercedes.
#Mumbai Indians have to score 175 in 20 overs to win against Kolkata Knight Riders..... Watching Rohit Sharma batting is soothing my eyes.....:-):-)
#BlackBerry planning to launch two new mid-range Android smartphones.
#Sennheiser looks to set up stores in India.
#Uber expands to more cities in China
#iOS 10 has smarter Siri, revamped Photos app, iMessages and more

input = "Sennheiser looks to set up stores in India."
a,s,d,f,g,h,j = imp_parsing(input)
print(a)
print(s)
print(d)
print(f)
print(g)
print(h)
print(j)

# str = str.split("\n")
words = []
for i in str:
    f = i.split()
    if f[7] == 'NAME':
        names_words.append(f[1])
print(names_words)
# for i in words:
#     if i in word_features:
#         print()

if names_words == []:
    print("General")
st = raw_input()
print st
for i in names_words:
    if query(i) != []:
        print(load_classifier_NBC("NBC_Categorization1.pickle").classify(find_features(query(i))))
    else:
        print("General")

# text = "(all_words_Movies.txt"
# print(text.strip("all_words_"))

# entity_similarity()