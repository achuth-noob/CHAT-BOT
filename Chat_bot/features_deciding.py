import nltk
from nltk.corpus import state_union

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
    features = []
    for l,i in enumerate(f):
        for j in decide_features(i.strip("\n"),num):
            features.append(j)
    return features

for i in run("temp_classification.txt",500):
    print(i)

