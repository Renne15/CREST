import json
import pandas as pd

filepath_json = "./data/output.json"
filepath_txt = "./data/EMS_358_20171016.txt"

with open(filepath_json, 'r') as readjson:
    data_json = {i : json.loads(line) for i, line in enumerate(readjson)}

with open(filepath_txt, 'r') as readtxt:
    data_txt = readtxt.read()

txt_lines = sum(1 for line in open(filepath_txt))

### sentence[]内にwordを入れる ###
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
        elif word == 'A':
            word += moji
        elif word == 'e':
            word += moji
        elif word == 'e.g':
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
    elif moji == '-':
        if word == '1':
            sentence.append(word)
            sentence.append('-')
            word = ''
        else:
            word += moji
    elif moji != '\n':
        word += moji

print("ListSize:", len(sentence))
print("51 instead:",sentence[51])
print("159 and:",sentence[159])
print("261 when:",sentence[261])
print("420 when:",sentence[420])
print("519 when:",sentence[519])
print("819 and:",sentence[819])
print("821 while:",sentence[821])
print("9428 and:",sentence[9428])

#print("9438 finaly:",sentence[9438])

conn = {}
Token_Arg1 = {}
Token_Arg2 = {}
for line, value in data_json.items():
    if value["Connective"]["TokenList"]:
        conn[value["Connective"]["TokenList"][0]] = {}
        conn[value["Connective"]["TokenList"][0]]["conn_name"] = value["conn_name"]
        conn[value["Connective"]["TokenList"][0]]["sense"] = value["Sense"][0]
    if len(value["Connective"]["TokenList"]) == 2:
        conn[value["Connective"]["TokenList"][1]] = {}
        conn[value["Connective"]["TokenList"][1]]["conn_name"] = value["conn_name"]
        conn[value["Connective"]["TokenList"][1]]["sense"] = value["Sense"][0]
    if "conn_name" in value:
        for arg1 in value["Arg1"]["TokenList"]:
            Token_Arg1[arg1] = value["Connective"]["TokenList"]
        for arg2 in value["Arg2"]["TokenList"]:
            Token_Arg2[arg2] = value["Connective"]["TokenList"]

### HTMLファイルとして書き出し ###
f = open("./data/sentence.html",'w')
f.write("<!DOCTYPE HTML>\n")
f.write("<html>\n")
f.write("<head>\n")
f.write("<title>CREST</title>\n")
f.write("</head>\n")
f.write("<body>\n")
word_num = 0
for i in range(txt_lines):
    f.write("<p>")
    while sentence[word_num] != '.':
        if word_num in conn:
            color = "blue"
            f.write("<font color=\"%s\"><strong title=\"%s\">" % (color,conn[word_num]["sense"]) +sentence[word_num]+"</strong></font>" )
            f.write(" ")
            word_num += 1
        elif word_num in Token_Arg1:
            f.write("<u>"+sentence[word_num]+"</u>")
            f.write("<u> </u>")
            word_num += 1
        elif word_num in Token_Arg2:
            f.write("<u>"+sentence[word_num]+"</u>")
            f.write("<u> </u>")
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
