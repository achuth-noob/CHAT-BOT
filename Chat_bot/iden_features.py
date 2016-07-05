import nltk
import nlpnet

features = []
def dependency_parse(input):
    parser = nlpnet.DependencyParser('C:/Users/test/Desktop/NLP/dependency', language='en')
    parsed_text = parser.parse(input)
    sent = parsed_text[0]
    return str(sent.to_conll())

def iden_com_names(input):
    pos = nltk.pos_tag(nltk.word_tokenize(input))
    print(pos)
    f = open("cab_company_names.txt", 'r')
    comp_names = []
    for i,l in  enumerate(f):
        comp_names.append(l.strip())
    print(comp_names)
    dep = dependency_parse(input)
    print(dep)
    dep = dep.split("\n")
    com_name = 0
    com_name_sub=0
    com_name_obj = 0
    for i in pos:
        if i[1] == "NN" or i[1] == "NNP" or i[1] == "NNS":
            if i[0] in comp_names:
                com_name = 1
    if com_name ==1:
        list = []
        for l in dep:
            list.append(l.split())
        for l in range(len(list)):
            if list[l][1] in comp_names:
                if list[l][7]== "SBJ" or list[l+1][7]== "SBJ":
                    com_name_sub = 1
                else:
                    com_name_obj =1

    return [com_name,com_name_sub,com_name_obj]

input = "I want to book an Ola cab for a ride.e"
print(iden_com_names(input))
features.append("")