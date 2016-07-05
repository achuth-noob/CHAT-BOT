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

dic = [".", ",", "#", "(", ")", "{", "}", "'ve", "is", "am", "are", "of", "and", "from", "for", "the", "to", "--", ";", ":", "..."]

def POS_tagging(text):
    sample_text = text
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
#i hav lft behind many f my dreams to achieve this Olympic Gold.
#Yuzi's 2-25 & Rahul's 63* helped India seal the whitewash with a 10 wicket win!

# input = "Dorothy needs new shoes."
# input = "good job messi"
# names = name_ent_recog(input)
# print(names[0])
# names_words = []
# for i in names[0]:
#     if str(i).find("PERSON")!=-1:
#         i = str(i).strip("(PERSON").strip(")")
#         string = ""
#         i = i.split()
#         for j in i:
#             string = string + j.split("/")[0] + " "
#         print(string)
#         names_words.append(string)
#     if str(i).find("ORGANIZATION")!=-1:
#         i = str(i).strip("(ORGANIZATION").strip(")")
#         string = ""
#         i = i.split()
#         for j in i:
#             string = string + j.split("/")[0] + " "
#         print(string)
#         names_words.append(string)
#     if str(i).find("GPE") != -1:
#         i = str(i).strip("(GPE").strip(")")
#         string = ""
#         i = i.split()
#         for j in i:
#             string = string + j.split("/")[0] + " "
#         print(string)
#         names_words.append(string)
#

# str = dependency_parse(input)
# print (str)

# str = str.split("\n")
# words = []
# for i in str:
#     f = i.split()
#     if f[7] == 'NAME':
#         names_words.append(f[1])
# print(names_words)
# for i in words:
#     if i in word_features:
#         print()
#
# if names_words == []:
#     print("General")

# for i in names_words:
#     if query(i) != []:
#         print(load_classifier_NBC("NBC_Categorization1.pickle").classify(find_features(query(i))))
#     else:
#         print("General")

# text = "(all_words_Movies.txt"
# print(text.strip("all_words_"))

# entity_similarity()

#That Messi nutmeg on the keeper had check level x99999999
#Gujarat CM Anandiben Patel faced protest by Patidar women at Hardik Patel's hometown Viramgam.
#Chief minister Pinarayi Vijayan confirms the arrest of Assam native who killed Jisha in Perumbavur
#Police put Patidar reservation stir leader Hardik Patel's family under house arrest due to CM's program in Viramgam.
#i hav lft behind many f my dreams to achieve this Olympic Gold.
#Yuzi's 2-25 & Rahul's 63* helped India seal the whitewash with a 10 wicket win!

# input = "Chief minister Pinarayi Vijayan confirms the arrest of Assam native who killed Jisha in Perumbavur"

# pos_tagged = POS_tagging(input)
# dep = dependency_parse(input)
#
# for i in pos_tagged:
#     print(i)
# print(dep)
# #
# # f = open("Verb_features_removed.txt","r")
# # features = []
# # for l,i in enumerate(f):
# #     features.append(i)
#
#
# primary = ""
# secondary = ""

# b = nltk.grammar
# grammar = nltk.PCFG.fromstring("""
#     S
#     VP
#     VP
#     TV
#     IV
#     DatV
#     NP
#     NP
# """)
#
# v = nltk.ViterbiParser()

# print(nltk.parse.malt.MaltParser().parse(input))



# sentence = "Ellen alerted Helen."
# d = dependency_parse(sentence)
# print(d)
# tokens = nltk.word_tokenize(sentence)
# tagged = nltk.pos_tag(tokens)
# entities = nltk.chunk.ne_chunk(tagged)
# from nltk.corpus import treebank
# t = treebank.parsed_sents()[0]
# print(t.draw())

# from nltk.parse import RecursiveDescentParser
# from nltk.grammar import PCFG, induce_pcfg, toy_pcfg1, toy_pcfg2
# grammar = toy_pcfg2
# rd = RecursiveDescentParser(grammar)
# sentence  = sentence.split()
# # for t in rd.parse(sentence):
# #      print(t)
#
# fcp2 = nltk.parse.load_parser('grammars/book_grammars/feat0.fcfg')
# for t in fcp2.parse(sentence):
#      print(t)
# import os
# from nltk.parse import stanford
#
# nltk.internals.config_java("C:/Program Files (x86)/Java/jre1.8.0_6/bin/java.exe")
# # java_path = "C:/Program Files (x86)/Java/jre1.8.0_6/binjava.exe"
# # os.environ['JAVAHOME'] = java_path
# os.environ['STANFORD_PARSER'] = 'D:/Downloads/stanford-parser-full-2015-12-09/stanford-parser.jar'
# os.environ['STANFORD_MODELS'] = 'D:/Downloads/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar'
#
# parser = stanford.StanfordParser(model_path="englishPCFG.ser.gz")
# sentences = parser.raw_parse_sents(("Hello, My name is Melroy.", "What is your name?"))
# print sentences
# #
# # GUI
# for line in sentences:
#     for sentence in line:
# #         sentence.draw()
#
# import jsonrpclib
# from simplejson import loads
# server = jsonrpclib.Server("http://localhost:8080")
#
# result = loads(server.parse("Hello world.  It is so beautiful"))
# print("Result", result)
# import pexpect
# from corenlp import StanfordCoreNLP
# corenlp_dir = "D:/Downloads/stanford-corenlp-full-2015-12-09"
# corenlp = StanfordCoreNLP(corenlp_dir)# wait a few minutes...
# corenlp.raw_parse("I love you bitch")
# d = pexpect.spawn()

# import requests
#
# r= requests.get("http://nlp.stanford.edu:8080/parser/index.jsp")
# print(r.content)
#
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
#
# driver = webdriver.Firefox()
# driver.get("http://nlp.stanford.edu:8080/parser/index.jsp")
# inputElement = driver.find_element_by_id("query")
# inputElement.send_keys(' I like a good amount of money')
# # inputElement.send_keys(Keys.ENTER)
# inputElement.submit()
#
# driver.get('http://www.w3c.org')
# element = driver.find_element_by_name('q')
# element.send_keys('hi mom')
#
# element_text = element.text
# element_attribute_value = element.get_attribute('value')
#
# print element
# print 'element.text: {0}'.format(element_text)
# print 'element.get_attribute(\'value\'): {0}'.format(element_attribute_value)
# driver.quit()
#----------------------------------------Parser-------------------------------------------------
# from pattern.en import parse
# from pattern.en import pprint
# input = 'Achuth is the best guy'
# s = parse(input, relations=True, lemmata=True)
# pprint(s)
# print(parse(input).split())

#----------------------------------------Conversion of verbs into present tense-----------------------------------------
# from nltk.stem.wordnet import WordNetLemmatizer
# words = ['gave','went','going','dating','conjuring']
# for word in words:
#     print word+"-->"+WordNetLemmatizer().lemmatize(word,'v')

#----------------------------------------


























