import json
from SPARQLWrapper import SPARQLWrapper
import urllib.parse
import requests
import time
import sys
import argparse

rows = {}



endpoint = "https://jpsearch.go.jp/rdf/sparql"

sparql = SPARQLWrapper(endpoint=endpoint, returnFormat='json')

# time.sleep(1)

q = ("""
    PREFIX jps: <https://jpsearch.go.jp/term/property#>
    PREFIX schema: <http://schema.org/>
    PREFIX type: <https://jpsearch.go.jp/term/type/>
    PREFIX chname: <https://jpsearch.go.jp/entity/chname/>
    PREFIX dct: <http://purl.org/dc/terms/>
    SELECT distinct ?license ?category ?label WHERE {
        ?license dct:isVersionOf?/schema:category ?category .
        ?s jps:accessInfo/schema:license ?license . 
        ?category rdfs:label ?label . 
    }
""")

# optional { ?p schema:name ?name . filter(lang(?name) = "en") } ?name 

sparql.setQuery(q)

url = endpoint+"?query="+urllib.parse.quote(q)+"&format=json&output=json&results=json"

r = requests.get(url)

# 結果はJSON形式なのでデコードする
results = json.loads(r.text)

for i in range(len(results["results"]["bindings"])):
    obj = results["results"]["bindings"][i]

    if i == 0:
        print(obj)

    s = obj["license"]["value"]

    if s not in rows:
        rows[s] = []

    rows[s].append({
        "label" : obj["label"]["value"],
        "uri" : obj["category"]["value"]
    })

fw = open("data/pre/101_licenses.json", 'w')
json.dump(rows, fw, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

# print(rows)
