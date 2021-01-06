collection=$1
id=$2
skipFlag=$3

echo "001_create_list.py"
python 001_create_list.py $collection $id
echo "002_downloader.py"
python 002_downloader.py $id $skipFlag
# echo "003_get_es.py"
# python 003_get_es.py $id $skipFlag
echo "004_create_rdf.py"
python 004_create_rdf.py $id $skipFlag
echo "005_entites.py"
python 005_entities.py $id $skipFlag
echo "006_mod_rdf.py"
python 006_mod_rdf.py $id $skipFlag