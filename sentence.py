import json
import pandas as pd

filepath_json = "./data/output.json"
filepath_txt = "./data/EMS_358_20171016.txt"

with open(filepath_json, 'r') as readjson:
    data_json = {i : json.loads(line) for i, line in enumerate(readjson)}

with open(filepath_txt, 'r') as readtxt:
    data_txt = readtxt.read()

sentence = []
word = ''
for moji in data_txt:
    if moji == ',':
        if word != '':
            sentence.append(word)
            word = ''
        sentence.append(',')
    elif moji == '.':
        if word == 'C':
            word += moji
        elif word == 'B':
            word += moji
        else:
            if word != '':
                sentence.append(word)
                word = ''
            sentence.append('.')
    elif moji == ' ':
        if word != '':
            sentence.append(word)
            word = ''
    elif moji == '(':
        if word != '':
            sentence.append(word)
            word = ''
        sentence.append('(')
    elif moji == ')':
        if word != '':
            sentence.append(word)
            word = ''
        sentence.append(')')
    # elif moji == '/':
    #     if word != '':
    #         sentence.append(word)
    #         word = ''
    #         sentence.append('/')
    elif moji != '\n':
        word += moji

# print("51 instead:",sentence[51])
# print("159 and:",sentence[159])
# print("261 when:",sentence[261])
# print("420 when:",sentence[420])
# print("519 when:",sentence[519])
# print("819 and:",sentence[819])
# print("821 while:",sentence[821])
# print("9428 and:",sentence[9428])
#
# print("9438 finaly:",sentence[9438])

conn = {}
for line, value in data_json.items():
    if value["Connective"]["TokenList"]:
        conn[value["Connective"]["TokenList"][0]] = {}
        conn[value["Connective"]["TokenList"][0]]["conn_name"] = value["conn_name"]
        conn[value["Connective"]["TokenList"][0]]["sense"] = value["Sense"][0]

# for line, value in data_json.items():
#     if "conn_name" not in value:
#         pass
#     else:
#         conn[line] = {}
#         conn[line]["conn_name"] = value["conn_name"]
#         conn[line]["sense"] = value["Sense"][0]
#         conn[line]["Connective"] = value["Connective"]["TokenList"][0]

f = open("./data/sentence.html",'w')
f.write("<!DOCTYPE HTML>\n")
f.write("<html>\n")
f.write("<head>\n")
f.write("<title>CREST</title>\n")
f.write("</head>\n")
f.write("<body>\n")
word_num = 0
for i in range(20):
    f.write("<p>")
    while sentence[word_num] != '.':
        if word_num in conn:
            f.write("<font color=\"blue\">"+sentence[word_num]+"</font>")
            f.write(" ")
            word_num += 1
        else:
            f.write(sentence[word_num])
            f.write(" ")
            word_num += 1
    f.write(sentence[word_num])
    word_num += 1
    f.write("</p>\n")
f.write("</body\n")
f.write("</html>\n")
f.close()
