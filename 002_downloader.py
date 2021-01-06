import sys
import csv
import argparse
import os
from SPARQLWrapper import SPARQLWrapper
import requests
import urllib.parse
import time
import json

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('filename', help='ファイル名')    # 必須の引数を追加
parser.add_argument('skip_flg', help='True or False')

args = parser.parse_args()    # 4. 引数を解析

query = """
    define sql:describe-mode "CBD"
    DESCRIBE <{uri}>
	<{uri}#accessinfo>
	<{uri}#sourceinfo>
    """

endpoint_url = "https://jpsearch.go.jp/rdf/sparql"

skip_flg = True if args.skip_flg == "True" else False

list_path = "data/001_csv/"+args.filename+".csv"

with open(list_path, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # ヘッダーを読み飛ばしたい時
    
    uris = []

    for row in reader:
        uri = row[0]
        uris.append(uri)

    for i in range(len(uris)):

        uri = sorted(uris)[i]
        
        name = uri.split("/")[-1]

        if i % 100 == 0:
            print(i+1, len(uris), name)

        prefix = name.split("-")[0]

        opath = "data/002_json/"+prefix+"/"+name+".json"

        if os.path.exists(opath) and skip_flg:
            continue

        dirname = os.path.dirname(opath)
        os.makedirs(dirname, exist_ok=True)

        '''
        sparql = SPARQLWrapper(endpoint_url, returnFormat='json')
        q = query.format(uri=uri)
        sparql.setQuery(q)

        url = endpoint_url+"?query=" + \
            urllib.parse.quote(q)+"&format=json&output=json&results=json"
        '''

        try:
            results = requests.get(uri+".json").json()

            fw = open(opath, 'w')
            json.dump(results, fw, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))
        except Exception as e:
            time.sleep(1)
            print("Error", name, e)
            continue

