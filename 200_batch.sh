collection=$1
id=$2
silent=$3

# ダウンロードリスト（CSV）の作成
echo "001_create_list.py"
python 001_create_list.py --silent $silent $collection $id

# 利活用スキーマのダウンロード
echo "002_downloader.py"
python 002_downloader.py --silent $silent $id

# JSのJSONファイルのダウンロード（任意）
# echo "003_get_es.py"
# python 003_get_es.py --silent $silent $id

# ダウンロードしたデータのフォーマット変換
echo "004_create_rdf.py"
python 004_create_rdf.py --silent $silent --skip False $id

# Entity（人名、地名など）データのダウンロード
echo "005_entites.py"
python 005_entities.py --silent $silent $id

# アイテムとEntityデータの関連づけ
echo "006_mod_rdf.py"
python 006_mod_rdf.py --silent $silent --skip False $id