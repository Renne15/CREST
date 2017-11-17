import json
import pandas as pd

filePath_json = "../conll2015_discourse/data/output.json"

with open(filePath_json, 'r') as readjson:
    data_json = {i : json.loads(line) for i, line in enumerate(readjson)}

conn = {}
#conn_sense = {}
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
            sense[value["Sense"][0]]["conn"] = value["conn_name"]
    elif value["Sense"][0] in sense:
        sense[value["Sense"][0]]["count"] += 1
        if "conn_name" in value:
            if value["conn_name"] not in sense[value["Sense"][0]]["conn"]:
                sense[value["Sense"][0]]["conn"] += ', '+value["conn_name"]

conn_df = pd.DataFrame.from_dict(conn)
sense_df = pd.DataFrame.from_dict(sense)
conn_df = conn_df.T
sense_df = sense_df.T
conn_df.sort_values(by="count", ascending=False)
sense_df.sort_values(by="count", ascending=False)

print(conn_df)
print(sense_df)

conn_df.to_csv("data/conn.csv")
sense_df.to_csv("data/sense.csv")
