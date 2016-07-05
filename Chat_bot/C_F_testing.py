import nltk
import random
import gensim
import pickle
import wikipedia
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))
dic = [".", ",", "(", ")", "{", "}", "'ve", "is", "am", "are", "of", "and", "from", "for", "the", "to", "--", ";", ":", "..."]

def load_classifier_NBC(file):
   f = open(file, 'rb')
   classifier = pickle.load(f)
   f.close()
   return classifier

def POS_tagging(corpus):
    train_text = state_union.raw("2005-GWBush.txt")
    sample_text = corpus
    #print(train_text)
    custom_sentence_tokenizer = PunktSentenceTokenizer(train_text)

    # textfile = open("POS_tagged",'w')
    # textfile.write(train_text)
    # textfile.write("\n\n\n\n\n\n\n\n\n\n")
    # print(custom_sentence_tokenizer)

    tokenized = custom_sentence_tokenizer.tokenize(sample_text)
    tuples_list = []
    def process_content():
        try:
            for i in tokenized:
                words = nltk.word_tokenize(i)
                tagged = nltk.pos_tag(words)
                for w in tagged:
                    tuples_list.append(w)
        except Exception as e:
            c=0
            # print(str(e))
    process_content()
    return tuples_list
    # textfile.close()

def remove_non_ascii(corpus):
    str=""
    for i in corpus:
        if 32<=ord(i)<=57 or 65<=ord(i)<=90 or 97<=ord(i)<=122:
            str=str+i
    return str

def remove_stopwords(corpus):
    sen = sent_tokenize(remove_non_ascii(corpus))
    s = []
    for i in sen:
        s.append(i.lower())
    words = []
    for i in s:
        for j in word_tokenize(i):
            words.append(j)
    removed = []
    for i in words:
        if i not in stop_words:
            if i not in dic:
                removed.append(i)
    return removed

def read_file(address):
    file = open(address,'r')
    return file.read()

def entity_similarity(keyword):
    #print("Program has started")
    model = gensim.models.Word2Vec.load("D:\Data_NLP\wiki.en.text1.model")
    list = model.most_similar(keyword)
    #print(list)
    #print(wikipedia.summary(keyword))
    #print("\n")
    summary_list=""
    try:
        for i in list:
            try:
                summary_list=summary_list + wikipedia.summary(i[0])
            except:
                continue
    except Exception as e:
        c=0
        #print(e)
    return summary_list

add1 = 'C:/Users/test/Desktop/My Folder/Cricket/Sports_Cricket_data.txt'
add2 = 'C:/Users/test/Desktop/My Folder/Football/Sports_Football_data.txt'
str1 = read_file(add1)
str2 = read_file(add2)
str1 = remove_non_ascii(str1).lower()
str2 = remove_non_ascii(str2).lower()
all_words = []
for i in str1:
    for k in word_tokenize(i):
        if k not in stop_words:
            if k not in dic:
                all_words.append(lemmatizer.lemmatize(k))
for i in str2:
    for k in word_tokenize(i):
        if k not in stop_words:
            if k not in dic:
                all_words.append(lemmatizer.lemmatize(k))
all_words = nltk.FreqDist(all_words)
all_words = all_words.most_common(3000)
word_features = []
for i in all_words:
    word_features.append(i[0])
# print (word_features)

def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    # print(features)
    return features

classifier = load_classifier_NBC("NBC_Categorization.pickle")
input = "kabali"
input = input.lower()
POS_tup_list = POS_tagging(input)
pos_tup_list = []
l=0
for i in POS_tup_list:
    pos_tup_list.append((POS_tup_list[l][0].lower(),POS_tup_list[l][1]))
    l=l+1

# print(pos_tup_list)

for i in pos_tup_list:
    if i[1] == 'NNP' or i[1] == 'NNP' or i[1] == 'NN':
        print(classifier.classify(find_features(remove_stopwords(entity_similarity(i[0])))))

