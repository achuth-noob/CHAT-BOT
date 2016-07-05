import nltk
import random
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import state_union
from nltk.corpus import stopwords
from nltk.tokenize import PunktSentenceTokenizer

def greeting_detection(dict,greet_list):
    j = dict[0]
    k = dict[0]
    l = 0
    for i in dict:
        if len(dict)==1:
            if i[0].lower() in greet_list:
                return True
        else:
            if l != len(dict):
                k = dict[(l + 1) % len(dict)]
            if i[0].lower() in greet_list:
                if i[1] == 'JJ' and (k[1] == 'NNS'  or k[1] == 'NNP' or k[1] == 'VBD'):
                    return True
                if i[1] == 'NNP' and (k[1] == 'NNP' or k[1] == 'NNS'):
                    return True
                if (j[1] == 'VBP' or j[1] == 'VB') and i[1] == 'JJ' and k[1] == 'NN':
                    return True
                if (j[1] == 'NN' or j[1] == 'NNP') and i[1] == 'JJ' and k[1] == 'NN':
                    return True
            if l == 0:
                if i[0].lower() in greet_list:
                    if i[1] == 'NNP' and (k[1] == 'NN' or k[1] == 'EX'):
                        return True
        l=l+1
        j=i
    return False

def process_content(tokenized):
    try:
        dict = []
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            k=0
            for w in tagged:
                if w[1] != 'IN' and w[1]!='DT' and w[1]!='.' and w[1]!=':' and w[1]!=',' and w[1] !='PRP' and w[1] !='PRP$' and w[1] !='POS' and w[1] !='TO' and w[1] != 'CC':
                # if w[1] == 'NNP' or w[1] == 'JJ':
                # textfile.write(str(w))
                # textfile.write("\n")
                    print(w)
                    dict.append(w)
                k=k+1
        return dict
    except Exception as e:
        print(str(e))

def greeting_conditions_decision(corpus):
    stop_words = set(stopwords.words("english"))
    dict = [".", ",", "(", ")", "{", "}", "'ve", "is", "are", "of", "and", "from", "for", "the", "to", "--", ";", ":", "..."]
    sentence_tokens = sent_tokenize(corpus)
    words = [[] for i in range(len(sentence_tokens))]
    o = 0

    for s in sentence_tokens:
        x = word_tokenize(s)
        for i in x:
            if i not in stop_words:
                if len(i) > 2:
                    if i not in dict:
                        words[o].append(i)
        o = o + 1
    #print(words)

    sentences = []
    for i in words:
        temp = ""
        for c in i:
            temp = temp+c+" "
        sentences.append(temp.strip())


    # for z in words:
    #     print(z)
    #
    # print(stop_words)

    train_text = state_union.raw("2005-GWBush.txt")

    # print(train_text)
    custom_sentence_tokenizer = PunktSentenceTokenizer(train_text)
    textfile = open("POS_tagged", 'w')
    textfile.write(train_text)
    textfile.write("\n\n\n\n\n\n\n\n\n\n")
    # print(custom_sentence_tokenizer)
    textfile.close()

    dict = process_content(sentences)
    greet_list = ["hi", "hello", "congrats", "congratulations", "happy", "good", "hey", "warm", "nice", "hearty","merry","beautiful"]
    decide = greeting_detection(dict, greet_list)
    print("\n\n")
    print(decide)
    print("\n")

load1 = open('Greeting_category_data.txt','r')
# load2 = open('non_greeting_category.txt','r')
data1 = load1.read()
# data2 = load2.read()
data_split1 = data1.split("\n")
# data_split2 = str(data2.split("\n"))
# print(data_split1)
# labeled_data = ([(sentence1,'greeting') for sentence1 in data_split1]+[(sentence2,'general') for sentence2 in data_split2])
# random.shuffle(labeled_data)
greeting_conditions_decision("Happy Anniversary")
