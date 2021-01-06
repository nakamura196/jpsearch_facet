import json
from SPARQLWrapper import SPARQLWrapper
import urllib.parse
import requests
import time
import sys
import csv
import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('collections', help='chname以下の文字列を指定')    # 必須の引数を追加
parser.add_argument('filename', help='出力ファイル名')    # 必須の引数を追加

args = parser.parse_args()    # 4. 引数を解析

collections_str = args.collections

if collections_str == "all":
    target = None
else:
    target = "https://jpsearch.go.jp/entity/chname/"+collections_str

filename = args.filename

flg = True

page = 0

rows = []
rows.append(["cho"])

unit = 1000

endpoint = "https://jpsearch.go.jp/rdf/sparql"

sparql = SPARQLWrapper(endpoint=endpoint, returnFormat='json')

while (flg):

    print(page)

    # time.sleep(1)

    q = ("""
        PREFIX jps: <https://jpsearch.go.jp/term/property#>
        PREFIX schema: <http://schema.org/>
        SELECT distinct ?cho WHERE {
            ?cho jps:sourceInfo ?source . 
            """
            +('?source schema:provider <'+target+'> . ' if target != None else '')+
            """
        } limit """ + str(unit) + """ offset """ + str(unit * page) + """
    """)
    sparql.setQuery(q)

    url = endpoint+"?query="+urllib.parse.quote(q)+"&format=json&output=json&results=json"

    r = requests.get(url)

    # 結果はJSON形式なのでデコードする
    results = json.loads(r.text)

    if len(results["results"]["bindings"]) == 0:
        flg = False

    page += 1



    for i in range(len(results["results"]["bindings"])):

        obj = results["results"]["bindings"][i]

        if i == 0:
            print(obj["cho"]["value"])
        cho = obj["cho"]["value"]

        rows.append([cho])

    # break


f = open("data/001_csv/"+filename+".csv", 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()
