import os
import re
from nltk.corpus import verbnet as vbnet

thematic_roles = []
selres = []
semantics = []
themroles_dict = {}
semantics_dict = {}
selres_dict = {}
for file in os.listdir("D:/Downloads/new_vn"):
    if file.endswith(".xml"):
        # print(file.strip(".xml").split("-")[0])
        # s=str(vbnet.pprint(file.strip(".xml").split("-")[0]))
        l = vbnet.classids(file.strip(".xml").split("-")[0])
        if l!=[]:
            for i in l:
                t=2
                s = str(vbnet.pprint(i))
                # print(s)
                subclasses = s.split("Subclasses:")[1].split("Members")[0].strip()
                theme = s.split("Thematic roles:")[1].split("Frames")[0]
                seman = s.split("Semantics:")[1:]
                for j in seman:
                    k = j.split("\n")
                    for w in k:
                        if '*' in w:
                            if w.strip("        * ").split("(")[0] in semantics_dict:
                                semantics.append(w.strip("        * ").split("(")[0].strip())
                                continue
                            else:
                                semantics.append(w.strip("        * ").split("(")[0].strip())
                                semantics_dict[w.strip("        * ").strip()] = 1
                for j in theme.split("\n"):
                    if j != '' and j != '  ':
                        if j.strip("   *").find('[') != -1:
                            # print(i.strip("   *"))
                            if j.strip("   *").split('[')[0] in themroles_dict:
                                thematic_roles.append(j.strip("   *").split('[')[0].strip())
                                continue
                            else:
                                thematic_roles.append(j.strip("   *").split('[')[0].strip())
                                themroles_dict[j.strip("   *").split('[')[0].strip()] = 1
                            for k in j.strip("   *").split('[')[1].split(']')[0].split('+'):
                                if k != "":
                                    if k in selres_dict:
                                        selres.append(k.strip())
                                        continue
                                    else:
                                        selres.append(k.strip())
                                        selres_dict[k.strip()] = 1
                        elif j.strip("   *").find('[') == -1:
                            if j.strip("   *") in themroles_dict:
                                thematic_roles.append(j.strip("   *").strip())
                                continue
                            else:
                                thematic_roles.append(j.strip("   *").strip())
                                themroles_dict[j.strip("   *").strip()] = 1

                while(subclasses!="(none)"):
                    s = str(vbnet.pprint(subclasses.split(" ")[0]))
                    subclasses = s.split("Subclasses:")[1].split("Members")[0].strip()
                    theme = s.split("Thematic roles:")[1].split("Frames")[0]
                    seman = s.split("Semantics:")[1:]
                    for j in seman:
                        k = j.split("\n")
                        for w in k:
                            if '*' in w:
                                if w.strip("        * ").split("(")[0] in semantics_dict:
                                    semantics.append(w.strip("        * ").split("(")[0].strip())
                                    continue
                                else:
                                    semantics.append(w.strip("        * ").split("(")[0].strip())
                                    semantics_dict[w.strip("        * ").strip()] = 1
                    for j in theme.split("\n"):
                        if j != '' and j != '  ':
                            if j.strip("   *").find('[') != -1:
                                # print(i.strip("   *"))
                                if j.strip("   *").split('[')[0] in themroles_dict:
                                    thematic_roles.append(j.strip("   *").split('[')[0].strip())
                                    continue
                                else:
                                    thematic_roles.append(j.strip("   *").split('[')[0].strip())
                                    themroles_dict[j.strip("   *").split('[')[0].strip()] = 1
                                for k in j.strip("   *").split('[')[1].split(']')[0].split('+'):
                                    if k != "":
                                        if k in selres_dict:
                                            selres.append(k.strip())
                                            continue
                                        else:
                                            selres.append(k.strip())
                                            selres_dict[k.strip()] = 1
                            elif j.strip("   *").find('[') == -1:
                                if j.strip("   *") in themroles_dict:
                                    thematic_roles.append(j.strip("   *").strip())
                                    continue
                                else:
                                    thematic_roles.append(j.strip("   *").strip())
                                    themroles_dict[j.strip("   *").strip()] = 1

print(set(thematic_roles))
print(set(selres))
print(set(semantics))
print(themroles_dict)
print(semantics_dict)
print(selres_dict)

f = open("tmp/features_verbs.txt","a")
for i in set(thematic_roles):
    f.write(i)
    f.write("\n")
for i in set(semantics):
    f.write(i)
    f.write("\n")
for i in set(selres):
    f.write(i)
    f.write("\n")
f.close()
