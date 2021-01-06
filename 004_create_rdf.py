import sys
import csv
import argparse
import os
import requests
import urllib.parse
import time
import json
import glob

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('filename', help='ファイル名')    # 必須の引数を追加
parser.add_argument('skip_flg', help='True or False')

args = parser.parse_args()    # 4. 引数を解析

skip_flg = True if args.skip_flg == "True" else False

path = "data/002_json/"+args.filename+"/*.json"

files = glob.glob(path)

for i in range(len(files)):
    file = files[i]

    id = file.split("/")[-1].split(".")[0]

    if i % 100 == 0:
        print(i+1, len(files), id)

    prefix = id.split("-")[0]

    opath = "data/004_json_rdf/"+prefix+"/"+id+".json"

    if os.path.exists(opath) and skip_flg:
        continue

    dirname = os.path.dirname(opath)
    os.makedirs(dirname, exist_ok=True)

    with open(file) as f:
        df = json.load(f)

    map = {}
    graphs = df["@graph"]
    graphMap = {}
    for graph in graphs:
        graphId = graph["@id"]
        graphMap[graphId] = graph
    
    for graphId in graphMap:

        graph = graphMap[graphId]

        if id in graphId:
            if "#sourceinfo" in graphId:

                map["source"] = [graph["http://schema.org/provider"]["@id"]]
            elif "#accessinfo" in graphId:
                map["access"] = [graph["http://schema.org/provider"]["@id"]]

                if "http://schema.org/itemLocation" in graph:
                    map["itemLocation"] = [graph["http://schema.org/itemLocation"]["@id"]]
                
                if "http://schema.org/license" in graph:
                    map["license"] = [graph["http://schema.org/license"]["@id"]]
            else:
                if "http://schema.org/isPartOf" in graph:
                    map["isPartOf"] = [graph["http://schema.org/isPartOf"]["@id"]]

                if "@type" in graph:
                    map["type"] = [graph["@type"]]

                properteis = {
                    "http://schema.org/creator" : "agential",
                    "http://schema.org/publisher" : "agential",
                    "http://schema.org/contributor" : "agential",
                    "http://schema.org/temporal" : "temporal",
                    "http://schema.org/spatial" : "spatial",
                    "http://schema.org/inLanguage" : "inLanguage"
                }

                for p in properteis:
                    
                    if p in graph:

                        es_field = properteis[p]
                        if es_field not in map:
                            map[es_field] = []

                        uris = []
                        values = graph[p]
                        if type(values) is not list:
                            values = [values]
                        for value in values:
                            map[es_field].append(value["@id"])

    try:
        fw = open(opath, 'w')
        json.dump(map, fw, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))
    except Exception as e:
        time.sleep(1)
        print("Error", name, e)
        continue