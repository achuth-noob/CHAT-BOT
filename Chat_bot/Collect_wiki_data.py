import wikipedia

def save_summary_in_file(input):
    text = wikipedia.summary(input)
    #print(text)
    file = open("Sports_Cricket_data.txt",'a')
    file.write(text.encode('utf-8'))
    file.write("\n\n")
    file.close()

def read_file(address):
    file = open(address,"r")
    return file.read().split("\n")

address = "Sports_Cricket_queries.txt"
list = read_file(address)
#print(list)
l=0
for i in list:
    try:
        save_summary_in_file(i)
        print("processed query no: %d" % l)
    except:
        print("processed query no: %d" % l)
        continue
    l=l+1