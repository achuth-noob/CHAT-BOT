# import nltk
# groucho_dep_grammar = nltk.DependencyGrammar.fromstring("""
# 'shot' -> 'I' | 'elephant' | 'in'
# 'elephant' -> 'an' | 'in'
# 'in' -> 'pajamas'
# 'pajamas' -> 'my'""")
# pdp = nltk.ProjectiveDependencyParser(groucho_dep_grammar)
# sent = 'I shot an elephant in my pajamas'.split()
# trees = pdp.parse(sent)
# for tree in trees:
#     print(tree)

# from nltk.parse.stanford import StanfordParser

# english_parser = StanfordParser("stanford-parser.jar", "stanford-parser-3.6.0-models.jar")
# print(english_parser.raw_parse_sents(("this is the english parser test", "the parser is from stanford parser")))

import nlpnet
def dependency_parse(input):
    parser = nlpnet.DependencyParser('C:/Users/test/Desktop/NLP/dependency', language='en')
    parsed_text = parser.parse(input)
    sent = parsed_text[0]
    return str(sent.to_conll())
