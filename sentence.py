import json
import pandas as pd

filepath_json = "./data/output.json"
filepath_txt = "./data/EMS_358_20171016.txt"

with open(filepath_json, 'r') as readjson:
    data_json = {i : json.loads(line) for i, line in enumerate(readjson)}

with open(filepath_txt, 'r') as readtxt:
    data_txt = readtxt.read()

sentences = []
word = ''
for moji in data_txt:
    if moji == ',':
        if word != '':
            sentences.append(word)
            word = ''
        sentences.append(',')
    elif moji == '.':
        if word == 'C':
            word += moji
        elif word == 'B':
            word += moji
        else:
            if word != '':
                sentences.append(word)
                word = ''
            sentences.append('.')
    elif moji == ' ':
        if word != '':
            sentences.append(word)
            word = ''
    elif moji == '(':
        if word != '':
            sentences.append(word)
            word = ''
        sentences.append('(')
    elif moji == ')':
        if word != '':
            sentences.append(word)
            word = ''
        sentences.append(')')
    # elif moji == '/':
    #     if word != '':
    #         sentences.append(word)
    #         word = ''
    #         sentences.append('/')
    elif moji != '\n':
        word += moji

print("51 instead:",sentences[51])
print("159 and:",sentences[159])
print("261 when:",sentences[261])
print("420 when:",sentences[420])
print("519 when:",sentences[519])
print("819 and:",sentences[819])
print("821 while:",sentences[821])
print("9438 finaly:",sentences[9438])

conn = {}
sense = {}

for line, value in data_json.items():
    if "conn_name" not in value:
        pass
    elif value["conn_name"] not in conn:
        conn[value["conn_name"]] = {}
        conn[value["conn_name"]]["count"] = 1
        conn[value["conn_name"]]["sense"] = value["Sense"][0]
    elif value["conn_name"] in conn:
        conn[value["conn_name"]]["count"] += 1

    if value["Sense"][0] not in sense:
        sense[value["Sense"][0]] = {}
        sense[value["Sense"][0]]["count"] = 0
        sense[value["Sense"][0]]["conn"] = []
        if "conn_name" in value:
            sense[value["Sense"][0]]["conn"].append(value["conn_name"])
    elif value["Sense"][0] in sense:
        sense[value["Sense"][0]]["count"] += 1
        if "conn_name" in value:
            if value["conn_name"] not in sense[value["Sense"][0]]["conn"]:
                sense[value["Sense"][0]]["conn"].append(value["conn_name"])

conn_df = pd.DataFrame(conn, index=["count","sense"])
sense_df = pd.DataFrame(sense, index=["count","conn"])
conn_df = conn_df.T
sense_df = sense_df.T
conn_df = conn_df.sort_values(by=["count"], ascending=False)
sense_df = sense_df.sort_values(by=["count"], ascending=False)

print(conn_df)
print(sense_df)

# conn_df.to_csv("data/conn.csv")
# sense_df.to_csv("data/sense.csv")
