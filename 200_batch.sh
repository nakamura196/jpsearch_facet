collection=$1
id=$2
silent=$3

echo $id : $collection

echo "001_create_list.py"
python 001_create_list.py --silent $silent $collection $id

echo "002_downloader.py"
python 002_downloader.py --silent $silent $id

# echo "003_get_es.py"
# python 003_get_es.py --silent $silent $id

echo "004_create_rdf.py"
python 004_create_rdf.py --silent $silent $id

echo "005_entites.py"
python 005_entities.py --silent $silent $id

echo "006_mod_rdf.py"
python 006_mod_rdf.py --silent $silent $id