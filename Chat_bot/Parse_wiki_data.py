file = open("Wiki_player_data.txt","r")
data = file.read().split(" \xc2\xb7 ")
# print(len(data))
file1 = open("Sports_Cricket_queries.txt", 'a')

for i in data:
    file1.write(i)
    file1.write("\n")