import sys
import csv
import argparse
import os
import requests
import urllib.parse
import time
import json
import glob

parser = argparse.ArgumentParser(
    description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('filename', help='ファイル名')    # 必須の引数を追加
parser.add_argument('--skip', help='True or False')
parser.add_argument('--silent', help='True or False, Default False')
args = parser.parse_args()    # 4. 引数を解析

path = "data/002_json/"+args.filename+"/*.json"

skip_flg = False if args.skip != None and args.skip != "True" else True
silent_flg = True if args.silent == "True" else False

files = glob.glob(path)

for i in range(len(files)):
    file = files[i]

    id = file.split("/")[-1].split(".")[0]

    if i % 100 == 0 and not silent_flg:
        print(i+1, len(files), id)

    prefix = id.split("-")[0]

    opath = "data/003_json_items/"+prefix+"/"+id+".json"

    if os.path.exists(opath) and skip_flg:
        continue

    dirname = os.path.dirname(opath)
    os.makedirs(dirname, exist_ok=True)

    with open(file) as f:
        df = json.load(f)

    map = {}
    graphs = df["@graph"]

    for graph in graphs:
        graphId = graph["@id"]

        if id in graphId and "#sourceinfo" in graphId:
            sourceData = graph["https://jpsearch.go.jp/term/property#sourceData"]["@id"]

            try:
                results = requests.get(sourceData).json()

                fw = open(opath, 'w')
                json.dump(results, fw, ensure_ascii=False, indent=4,
                          sort_keys=True, separators=(',', ': '))
            except Exception as e:
                time.sleep(1)
                print("Error", id, e)
                continue
