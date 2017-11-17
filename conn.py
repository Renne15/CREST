import json
import pandas as pd

filePath_json = "../conll2015_discourse/data/output.json"

with open(filePath_json, 'r') as readjson:
    data_json = {i : json.loads(line) for i, line in enumerate(readjson)}

conn = {}
conn_sense = {}
sense = {}

for line, value in data_json.items():
    if "conn_name" not in value:
        pass
    elif value["conn_name"] not in conn:
        conn[value["conn_name"]] = 1
        conn_sense[value["conn_name"]] = value["Sense"][0]
    elif value["conn_name"] in conn:
        conn[value["conn_name"]] += 1

    if value["Sense"][0] not in sense:
        sense[value["Sense"][0]] = 0
    elif value["Sense"][0] in sense:
        sense[value["Sense"][0]] += 1

# print(conn)
# print(conn_sense)
# print(sense)

conn_df = pd.DataFrame([conn.values(), conn_sense.values()], index=["count","sense"], columns=conn.keys())
sense_df = pd.DataFrame(sense, index=["count"])

# print(conn_df)
# print(sense_df)

conn_df.to_csv("data/conn_name.csv")
sense_df.to_csv("data/sense.csv")
