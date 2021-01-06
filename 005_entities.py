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

uris = []

for file in files:
    with open(file) as f:
        df = json.load(f)

    for key in df:
        values = df[key]

        for uri in values:

            if uri not in uris:
                uris.append(uri)

endpoint = "https://jpsearch.go.jp/rdf/sparql"

sparql = SPARQLWrapper(endpoint=endpoint, returnFormat='json')

for i in range(len(uris)):
    uri = sorted(uris)[i]

    if i % 100 == 0 and not skip_flg:
        print(i+1, len(uris), uri)

    hash = hashlib.md5(uri.encode('utf-8')).hexdigest()

    opath = "data/005_entity/"+hash+".json"

    if os.path.exists(opath) and skip_flg:
        continue

    dirname = os.path.dirname(opath)
    os.makedirs(dirname, exist_ok=True)

    q = ("""
        PREFIX jps: <https://jpsearch.go.jp/term/property#>
        PREFIX schema: <http://schema.org/>
        select * where {
            <""" + uri + """> ?p ?o
        }
    """)

    sparql.setQuery(q)

    url = endpoint+"?query=" + \
        urllib.parse.quote(q)+"&format=json&output=json&results=json"

    result = requests.get(url).json()

    result = result["results"]["bindings"]

    resultMap = {}

    for obj in result:
        p = obj["p"]["value"]
        o = obj["o"]["value"]

        if p not in resultMap:
            resultMap[p] = []

        value = {
            "value": o,
        }

        # 言語情報
        if "xml:lang" in obj["o"]:
            value["lang"] = obj["o"]["xml:lang"]

        resultMap[p].append(value)

    label = ""

    if "http://www.w3.org/2000/01/rdf-schema#label" in resultMap:
        label = resultMap["http://www.w3.org/2000/01/rdf-schema#label"][0]["value"]

    # ラベルがない場合には、ローカル値を利用
    if label == "":
        label = uri.split("/")[-1]

    label_en = ""
    if "http://schema.org/name" in resultMap:
        values = resultMap["http://schema.org/name"]

        for value in values:
            if "lang" in value and value["lang"] == "en":
                label_en = value["value"]

    # 英語のラベルがなければ日本語
    if label_en == "":
        label_en = label

    entity = resultMap
    entity["uri"] = uri
    entity["ja"] = label
    entity["en"] = label_en

    try:
        fw = open(opath, 'w')
        json.dump(entity, fw, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))
        fw.close()
    except Exception as e:
        time.sleep(1)
        print("Error", uri, e)
        continue
