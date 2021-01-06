import sys
import csv
import argparse
import os
import requests
import urllib.parse
import time
import json
import glob
import hashlib
from SPARQLWrapper import SPARQLWrapper

parser = argparse.ArgumentParser(
    description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('filename', help='ファイル名')    # 必須の引数を追加
parser.add_argument('--skip', help='True or False')
parser.add_argument('--silent', help='True or False, Default False')

args = parser.parse_args()    # 4. 引数を解析

skip_flg = False if args.skip != None and args.skip != "True" else True
silent_flg = True if args.silent == "True" else False

prefix = args.filename

files = glob.glob("data/004_json_rdf/"+prefix+"/*.json")
# files = glob.glob("data/004_json_rdf/*/tfam_art_db-1381.json")

uris = []

for file in files:

    with open(file) as f:
        df = json.load(f)

    for key in df:
        values = df[key]

        for uri in values:

            if uri not in uris:
                uris.append(uri)

# ロード
entities = {}
for i in range(len(uris)):
    uri = sorted(uris)[i]

    if i % 100 == 0 and not silent_flg:
        print(i+1, len(uris), uri)

    hash = hashlib.md5(uri.encode('utf-8')).hexdigest()

    path = "data/005_entity/"+hash+".json"

    if not os.path.exists(path):
        print("Not exist", uri)
        continue

    with open(path) as f:
        df = json.load(f)

    entities[hash] = df

for file in files:

    id = file.split("/")[-1].split(".")[0]
    prefix = id.split("-")[0]
    opath = "data/006_es_rdf/"+prefix+"/"+id+".json"

    if os.path.exists(opath) and skip_flg:
        continue

    dirname = os.path.dirname(opath)
    os.makedirs(dirname, exist_ok=True)

    item = {}

    with open(file) as f:
        df = json.load(f)

    fields = ["access", "source", "agential",
              "spatial", "temporal", "itemLocation",
              "inLanguage", "type", "isPartOf",
              "category", "relatedLink"
              # "license"
              ]

    for field in fields:

        if field not in df:
            continue

        values = df[field]

        item[field+"_ja"] = []
        item[field+"_en"] = []
        item[field+"_uri"] = []

        for value in values:

            hash = hashlib.md5(value.encode('utf-8')).hexdigest()

            if hash not in entities:
                print("Not exist", value, hash)
                continue

            entity = entities[hash]

            # コレクションの判定
            if field == "isPartOf":
                collectionFlag = False
                if "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" not in entity:
                    continue

                types = entity["http://www.w3.org/1999/02/22-rdf-syntax-ns#type"]
                for t in types:
                    if t["value"] == "http://schema.org/Collection":
                        collectionFlag = True

                if not collectionFlag:
                    continue

            item[field+"_ja"].append(entity["ja"])
            item[field+"_en"].append(entity["en"])
            item[field+"_uri"].append(entity["uri"])

    try:
        fw = open(opath, 'w')
        json.dump(item, fw, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))
    except Exception as e:
        time.sleep(1)
        print("Error", uri, e)
        continue
