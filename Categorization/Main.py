import nltk
import nlpnet
import wikipedia
import pickle
from nltk.corpus import stopwords
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer


dic = [".", ",", "#", "(", ")", "{", "}", "'ve", "is", "am", "are", "of", "and", "from", "for", "the", "to", "--", ";", ":", "...","with","Rs"]
stop_words = set(stopwords.words("english")+dic)


def save_classifier_NBC(classifier,add):
    add = "D:/Data_NLP/Bag_of_words_data/"+add+".pickle"
    f = open(add, 'wb')
    pickle.dump(classifier, f, -1)
    f.close()

def load_classifier_NBC(file):
    file = "D:/Data_NLP/Bag_of_words_data/"+file+".pickle"
    f = open(file, 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier

def remove_non_ascii(corpus):
    str=""
    for i in corpus:
        if 32<=ord(i)<=122:
            str=str+i
    return str

def dependency_parse(input):
    parser = nlpnet.DependencyParser('C:/Users/test/Desktop/NLP/dependency', language='en')
    parsed_text = parser.parse(input)
    sent = parsed_text[0]
    return str(sent.to_conll())

#5 Android apps to boost office productivity
#4 best Android smartphones under Rs 15,000 with fingerprint scanner.


# pos = nltk.pos_tag(nltk.word_tokenize(input))
# for i in pos:
#     print(i)
# print(dependency_parse(input))

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

def filter_sentences(input):
    input = input.strip()
    s = str(dependency_parse(input))
    k = s.split("\n")
    keywords = []
    for i in range(len(k)):
        k[i] = k[i].split()
        if  k[i][7] == "SUBJ" or k[i][7] == "OBJ" or k[i][7] == "NMOD" or k[i][7] == "PMOD" or k[i][7] == "ROOT":
            if k[i][3] != "CD":
                keywords.append(k[i][1])
    removed_keywords = []
    for i in keywords:
        if i not in stop_words:
            removed_keywords.append(i)
    return removed_keywords

def sorting(fil_addr,cre_addr):
    fil_addr = "D:/Data_NLP/Bag_of_words_data/"+fil_addr
    fi = open(fil_addr,'r')
    con = []
    for l,i in enumerate(fi):
        con.append(i.strip("\n"))
    con.sort()
    cre_addr = "D:/Data_NLP/Bag_of_words_data/"+cre_addr
    f = open(cre_addr,'a')
    for item in con:
        f.write(item)
        f.write("\n")
    f.close()

# names = name_ent_recog(input)
# # print(names[0])
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

# print(name_ent_recog(input))
# for i in names_words:
#     print(i)
# print(filter_sentences(input))

# print(wikipedia.summary("Politics in South India",sentences=30))
# print(wikipedia.search("hardik pandhya"))
# ny = wikipedia.page("Android (operating system)")
# #
# print(ny.content)

#
# print(wikipedia.summary("Player (political)"))
# g = open("D:/Data_NLP/Bag_of_words_data/pol.txt","r")
# keywords = []
# for l,i in enumerate(g):
#     x = wikipedia.search(i.strip("\n"))
#     bow = ""
#     for i in x:
#         try:
#             bow = bow + wikipedia.summary(i)
#         except:
#             continue
#     for i in nltk.sent_tokenize(remove_non_ascii(bow)):
#         for j in filter_sentences(i):
#             keywords.append(j)
#     # keywords = nltk.FreqDist(keywords)
#     # word_features = list(keywords.keys())
#     # for i in word_features:
#     #     print(i)
#     g = nltk.pos_tag(keywords)
#     f = open("D:/Data_NLP/Bag_of_words_data/politics_unsorted.txt","a")
#     for i in g:
#         if "NN" in i[1] or "VB" in i[1] or "JJ" in i[1]:
#             f.write(str(i[0]))
#             f.write("\n")
#     f.close()
# keywords.sort()
# save_classifier_NBC(keywords,"Politics_sorted")

sorting("Movies_sorted.txt","Movies__sorted.txt")