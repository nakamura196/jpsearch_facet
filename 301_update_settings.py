import json
from SPARQLWrapper import SPARQLWrapper
import urllib.parse
import requests
import yaml

endpoint = "https://jpsearch.go.jp/rdf/sparql"

sparql = SPARQLWrapper(endpoint=endpoint, returnFormat='json')

q = ("""
    PREFIX jps: <https://jpsearch.go.jp/term/property#>
    PREFIX schema: <http://schema.org/>
    SELECT ?provider (count(?cho) as ?count) WHERE {
        ?cho jps:sourceInfo/schema:provider ?provider .
    } GROUP BY ?provider ORDER BY ?count
""")
sparql.setQuery(q)

url = endpoint+"?query="+urllib.parse.quote(q)+"&format=json&output=json&results=json"

results = requests.get(url).json()

settings = {}

for i in range(len(results["results"]["bindings"])):
    obj = results["results"]["bindings"][i]
    provider = obj["provider"]["value"]
    count = obj["count"]["value"]

    q = ("""
        PREFIX jps: <https://jpsearch.go.jp/term/property#>
        PREFIX schema: <http://schema.org/>
        SELECT DISTINCT ?cho ?label ?image WHERE {
            ?cho rdfs:label ?label ;  jps:sourceInfo/schema:provider <"""+provider+"""> .
            OPTIONAL {?cho schema:image ?image}
        } LIMIT 1
    """)

    sparql.setQuery(q)

    url = endpoint+"?query="+urllib.parse.quote(q)+"&format=json&output=json&results=json"

    items = requests.get(url).json()

    item = items["results"]["bindings"][0]
    uri = item["cho"]["value"]
    prefix = uri.split("https://jpsearch.go.jp/data/")[1].split("-")[0]

    provider_local = provider.split("/")[-1]
    
    print(i+1, len(results["results"]["bindings"]), prefix, provider_local, count)
    settings[prefix] = provider_local

with open("settings.yml", "w") as yf:
    yaml.dump(settings, yf, encoding='utf-8', allow_unicode=True, sort_keys=False)