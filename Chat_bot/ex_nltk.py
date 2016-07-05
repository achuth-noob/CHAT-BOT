# ----------------------Tokenizing---------------------------
# from nltk.tokenize import sent_tokenize,word_tokenize
# ex_text = "Hello Mr.Smith, how are you doing today? The weather is great and python is awesome. The sky is great"
#
# print(sent_tokenize(ex_text))
#
# print(word_tokenize(ex_text))


# ---------------------------Stopwords------------------------------------
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
#
# ex_sen = "This is an example sentence showing off stop words filtration."
# stop_words = set(stopwords.words("english"))
# print(stop_words)
# words = word_tokenize(ex_sen)
# print(words)
#
# filtered_sentence = []
#
# for i in words:
#     if i not in stop_words:
#         filtered_sentence.append(i)
#
# for i in filtered_sentence:
#     print(i)
#
# filtered_sentenc = [w for w in words if not w in stop_words]
#
# print(filtered_sentenc)
# print(stop_words)


#-----------------------------------------Stemming-----------------------------
# from nltk.tokenize import word_tokenize
# from nltk.stem import PorterStemmer
#
# ps = PorterStemmer()
#
# Example_words = ["Python","Pythoning","Pyhtoned","Pythonly","Pythoner"]
#
# for i in Example_words:
#     print(ps.stem(i))


#--------------------------partsofspeech Tagging------------------------------
# from nltk.corpus import state_union
# from nltk.tokenize import PunktSentenceTokenizer\
#
# def POS_tagging(corpus):
#     train_text = state_union.raw("2005-GWBush.txt")
#     sample_text = corpus
#     #print(train_text)
#     custom_sentence_tokenizer = PunktSentenceTokenizer(train_text)
#     # textfile = open("POS_tagged",'w')
#     # textfile.write(train_text)
#     # textfile.write("\n\n\n\n\n\n\n\n\n\n")
#     # print(custom_sentence_tokenizer)
#     tokenized = custom_sentence_tokenizer.tokenize(sample_text)
#     tuples_list = []
#     def process_content():
#         try:
#             for i in tokenized:
#                 words = nltk.word_tokenize(i)
#                 tagged = nltk.pos_tag(words)
#                 for w in tagged:
#                     tuples_list.append(w)
#         except Exception as e:
#             print(str(e))
#
#
#     process_content()
#     return tuples_list
#     # textfile.close()


#---------------------------POS Tagging after removing stop words----------------------------
#
# import nltk
# from nltk.corpus import state_union
# from nltk.tokenize import PunktSentenceTokenizer
# from nltk.corpus import stopwords
#
# stop_words = set(stopwords.words("english"))
# train_text = state_union.raw("2005-GWBush.txt")
# sample_text = state_union.raw("2006-GWBush.txt")
# # print(train_text)
# custom_sentence_tokenizer = PunktSentenceTokenizer(train_text)
# textfile = open("POS_tagged(1)",'w')
# textfile.write(train_text)
# textfile.write("\n\n\n\n\n\n\n\n\n\n")
# #print(custom_sentence_tokenizer)
# tokenized = custom_sentence_tokenizer.tokenize(sample_text)
#
# def process_content():
#     try:
#         count = 0
#         #stopped_sentenc = []
#         for i in tokenized:
#             words = nltk.word_tokenize(i)
#             filtered_sentenc = [w for w in words if not w in stop_words]
#             #for i in words:
#                 #if i in stop_words:
#                     #stopped_sentenc.append(i)
#             tagged = nltk.pos_tag(filtered_sentenc)
#             for w in tagged:
#                 textfile.write(str(w))
#                 textfile.write("\n")
#                 count = count + 1
#                 print(w)
#         #print stopped_sentenc
#         print count
#     except Exception as e:
#         print(str(e))
#
# process_content()
# textfile.close()
#


#------------------------------Chunking-----------------------------
# import nltk
# from nltk.corpus import state_union
# from nltk.tokenize import PunktSentenceTokenizer
#
# train_text = state_union.raw("2005-GWBush.txt")
# sample_text = state_union.raw("2006-GWBush.txt")
#
# custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
#
# tokenized = custom_sent_tokenizer.tokenize(sample_text)
#
# def process_content():
#     try:
#         for i in tokenized:
#             words = nltk.word_tokenize(i)
#             tagged = nltk.pos_tag(words)
#             chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP><NN>?}"""
#             chunkParser = nltk.RegexpParser(chunkGram)
#             chunked = chunkParser.parse(tagged)
#             chunked.draw()
#             #print(chunked)
#             #print(tagged)
#     except Exception as e:
#         print(str(e))
#
# process_content()

#------------------------------------Chinking----------------------------------
# import nltk
# from nltk.corpus import state_union
# from nltk.tokenize import PunktSentenceTokenizer
#
# train_text = state_union.raw("2005-GWBush.txt")
# sample_text = state_union.raw("2006-GWBush.txt")
#
# custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
#
# tokenized = custom_sent_tokenizer.tokenize(sample_text)
#
# def process_content():
#     try:
#         for i in tokenized:
#             words = nltk.word_tokenize(i)
#             tagged = nltk.pos_tag(words)
#             chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP.?>*<NN>?}"""
#             # chunkGram = r"""Chunk: {<.*>+}
#             #                     }<VB.?|IN|DT>+{"""
#             chunkParser = nltk.RegexpParser(chunkGram)
#             chunked = chunkParser.parse(tagged)
#             print(chunked)
#             #print(tagged)
#     except Exception as e:
#         print(str(e))
#
# process_content()



#--------------------------Name Entitiy Recognition----------------------

# import nltk
# from nltk.corpus import state_union
# from nltk import PunktSentenceTokenizer
#
# train_text = state_union.raw("2005-GWBush.txt")
# sample_text = "Give ur test string here"
#
# custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
# tokenized = custom_sent_tokenizer.tokenize(sample_text)
#
# def process_content():
#     try:
#         for i in tokenized:
#             words = nltk.word_tokenize(i)
#             tagged = nltk.pos_tag(words)
#             namedEnt = nltk.ne_chunk(tagged)
#             print(namedEnt)
#
#
#             # chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP.?>*<NN>?}"""
#             # # chunkGram = r"""Chunk: {<.*>+}
#             # #                     }<VB.?|IN|DT>+{"""
#             # chunkParser = nltk.RegexpParser(chunkGram)
#             # chunked = chunkParser.parse(tagged)
#             # print(chunked)
#             # #print(tagged)
#     except Exception as e:
#         print(str(e))
#
# process_content()
#
#

#------------------------------------Lemmatizing-------------------------------------
#gives the synonym or the nearer word to the original word
# from nltk.stem import WordNetLemmatizer
#
# lemmatizer = WordNetLemmatizer()
#
# print(lemmatizer.lemmatize("hello"))
# # print(lemmatizer.lemmatize("cacti"))
# # print(lemmatizer.lemmatize("geese"))
# # print(lemmatizer.lemmatize("rocks"))
# # print(lemmatizer.lemmatize("pythons"))
#
# print(lemmatizer.lemmatize("better",pos="a"))
# print(lemmatizer.lemmatize("best",pos = "a"))
# print(lemmatizer.lemmatize("run"))
# #Lemmatizing is better than the stemming

#-------------------------------------Corpora----------------------------------

# from nltk.corpus import gutenberg
# from nltk.tokenize import sent_tokenize
#
# sample = gutenberg.raw("bible-kjv.txt")
#
# tok = sent_tokenize(sample)
#
# for i in tok[5:15]:
#     print(i)

#---------------------------------WordNet------------------------------------------

# from nltk.corpus import wordnet
#
# syns = wordnet.synsets("football")
# #
# for i in syns:
#     print(i)
# ##synonyms of the word
# # print(syns[3].lemmas()[3].name())
#
# # print("\n\n")
# # #definition of the word
# # print(syns[0].definition())
# # print("\n")
#
# # #Examples to the particular word
# # print(syns[0].examples())
#
# synonym = []
# antonyms = []
#
# for i in wordnet.synsets("welcome"):
#     for l in i.lemmas():
#         synonym.append(l.name())
#         if l.antonyms():
#             antonyms.append(l.antonyms()[0].name())
#
# synonym = set(synonym)
# antonyms = set(antonyms)
#
# for i in synonym:
#     print(i)
#
# print("\n\n\n\n\n")
#
# for i in antonyms:
#     print(i)

#------------------------------Classification-----------------
# import nltk
# import random
# from nltk.corpus import movie_reviews
#
# # documents = [(list(movie_reviews.words(fileid)),category)
# #              for category in movie_reviews.categories()
# #              for fileid in movie_reviews.fileids(category)]
#
# documents = []
# for category in movie_reviews.categories():
#     for fileid in movie_reviews.fileids(category):
#         documents.append((list(movie_reviews.words(fileid)),category))
#
# # print(set(movie_reviews.words('neg/cv000_29416.txt')))
# # print(documents)
#
# random.shuffle(documents)
# all_words = []
# # print(movie_reviews.words())
#
# for w in movie_reviews.words():
#     all_words.append(w.lower())
#
# # print(all_words)
#
# all_words = nltk.FreqDist(all_words)
# # print(type(all_words))
# word_features = list(all_words.keys())[:3000]
#
# def find_features(document):
#     words = set(document)
#     features = {}
#     for w in word_features:
#         features[w] = (w in words)
#     return features
#
# # print(movie_reviews.words('pos/cv000_29590.txt'))
#
# for i in (find_features(movie_reviews.words('pos/cv000_29590.txt'))):
#      print(i,find_features(movie_reviews.words('pos/cv000_29590.txt'))[i])
#
# # print(type(find_features(movie_reviews.words('neg/cv000_29416.txt'))))

#-------------------------Twitter login-------------------------
# import tweepy
# from time import sleep
# consumer_key = 'e7tEgv4tPKOLNA6OHPNaWP6C3)'
# consumer_secret = 'Hi35zmP18dBqhz1iO8Z1YWMLgmHKOaLyDWDkE0pURmjQ4vzQtm'
# access_token = '732101075507937281-MDR5veLDxsVm2loGhrPidIENFwhZYv5'
# access_token_secret = 'Paf41KiEqtwnpa3cPamBl0OfHZHByDzzV7T6eJp0Qs67V'
#
# auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# auth.secure = True
# api = tweepy.API(auth,secure=True)
#
# print(str(api.get_user(screen_name = '@Achuth_123')))

#----------------------------Chat Bot for twitch----------------------------
# import socket
# import string
# from settings import HOST, PORT, PASS,IDENTITY,CHANNEL
#
# def joinRoom(s):
#     readbuffer = ""
#     Loading = True
#     while Loading:
#         readbuffer = readbuffer + s.recv(1024)
#         temp = string.split(readbuffer, "\n")
#         readbuffer = temp.pop()
#
#         for line in temp:
#             print(line)
#             Loading = loadingComplete(line)
#
#     sendMessage(s,"Suceessfully joined chat")
#
# def loadingComplete(line):
#     if("End of /NAMES list" in line):
#         return False
#     else:
#         return True
#
# def opensocket():
#     s = socket.socket()
#     s.connect((HOST,PORT))
#     s.send("PASS " + PASS + "\r\n")
#     s.send("NICK " + IDENTITY + "\r\n")
#     s.send("JOIN #" + CHANNEL + "\r\n")
#     return s
#
# def sendMessage(s, message):
#     messagetemp = "PRIVMSG" + CHANNEL + " :" + message
#     s.send(messagetemp + "\r\n")
#     print("test" + messagetemp)
#
# s = opensocket()
# joinRoom(s)
#
# while True:
#     persist = True



#-----------------------------------Word2vec-------------------------------------

# import gensim, logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# sentences = [['first', 'sentence'], ['second', 'sentence']]
# model = gensim.models.Word2Vec(sentences, min_count=1)
#
# class MySentences(object):
#     def __init__(self, dirname):
#         self.dirname = dirname
#
#     def __iter__(self):
#         for fname in os.listdir(self.dirname):
#             for line in open(os.path.join(self.dirname, fname)):
#                 yield line.split()
#
# sentences = MySentences('/some/directory') # a memory-friendly iterator
# model = gensim.models.Word2Vec(sentences)
#
# model = gensim.models.Word2Vec() # an empty model, no training


#-----------------------------------Words as Features for learning--------------------------------
# import nltk
# import random
# from nltk.corpus import movie_reviews
# from nltk.tokenize import sent_tokenize,word_tokenize
# from nltk.corpus import state_union
# from nltk.corpus import stopwords
# from nltk.tokenize import PunktSentenceTokenizer
#
# stop_words = set(stopwords.words("english"))
# corpus = """Happy birthday to you"""
#
# #print(corpus)
#
# stop_words = set(stopwords.words("english"))
#
# dict = [".",",","(",")","{","}","'ve","is","are","of","and","from","for","the","to","--",";",":","..."]
# sentence_tokens = sent_tokenize(corpus)
#
# words = [[] for i in range(len(sentence_tokens))]
#
# o=0
# for s in sentence_tokens:
#     x = word_tokenize(s)
#     for i in x:
#         if i not in stop_words:
#             if len(i)>2:
#                 if i not in dict:
#                     words[o].append(i)
#     o = o+1
#
#
# documents = [(list(movie_reviews.words(fileid)),category)
#              for category in movie_reviews.categories()
#              for fileid in movie_reviews.fileids(category)]
#
# for i in documents:
#     print(i)

#print(set(movie_reviews.words('neg/cv000_29416.txt')))
# random.shuffle(documents)
# all_words = []
#
# for w in movie_reviews.words():
#     all_words.append(w.lower())
#
# all_words = nltk.FreqDist(all_words)
#
# word_features = list(all_words.keys())[:3000]
#
# def find_features(document):
#     words = set(document)
#     features = {}
#     for w in word_features:
#         features[w] = (w in words)
#     return features
#
# #print((find_features(movie_reviews.words('neg/cv000_29416.txt'))))FPO
#
# featuresets = [(find_features(rev), category) for (rev, category) in documents]
#
# training_set = featuresets[:1900]
# testing_set = featuresets[1900:]
#
# classifier = nltk.NaiveBayesClassifier.train(training_set)
# #print("Naive Bayes Algo accuracy:", (nltk.classify.accuracy(classifier,testing_set))*100)
# classifier.show_most_informative_features(15)

#---------------------------------Word Categorizing--------------------------------
# import nltk
# from nltk.corpus import brown
#
# tagged_token = nltk.tag.str2tuple('fly/V')
# print(tagged_token)


#-----------------------------------Dependency Parser-----------------------------------------
# from nltk.parse.stanford import StanfordDependencyParser
# path_to_jar = "stanford-parser.jar"
# path_to_models_jar = 'stanford-parser-3.6.0-models.jar'
# # k=0
# # for i in path_to_jar:
# #     if i=='/':
# #         path_to_jar[k]=
# dependency_parser = StanfordDependencyParser(path_to_jar, path_to_models_jar)
#
# result = dependency_parser.raw_parse('I shot an elephant in my sleep')
# # dep = result.next()
# # print(list(dep.triples()))
#

import wikipedia
print(wikipedia.summary("sports cristiano"))











