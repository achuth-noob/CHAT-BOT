file = open("Unformatted_Sports_volleyball_queries.txt","r")
str = file.read().split("\n")
f = open("Sports_volleyball_queries.txt","a")
country_dic = ["poland","italy","united","states","netherlands",
               "philippines","cuba","turkey","dominican republic",
               "brazil","japan",
               "spain","bulgaria","russia","india","serbia","iran",
               "finland","canada","france","argentina","czech republic","germany","belgium"
               "dominican republic","hristo","netherlands/israel","thailand"]
for i in str:
    words = i.split()
    temp=""
    if words[0].lower() in country_dic:
        for j in words[1:]:
            temp = temp + j + " "
        f.write(temp)
        f.write("\n")
        continue
    f.write(i)
    f.write("\n")

f.close()