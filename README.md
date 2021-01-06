# Japan Search Facet Generator

ジャパンサーチの利活用スキーマから、ファセット検索用のデータを作成するプログラムです。

## Installation

Requirements:

- Python 3

Install latest release:

```
pip install -r requirements.txt
```

## Usage

以下を実行してください。

```
sh 201_batches.sh
```

実行後、 `data/006_es_rdf` にファイルが出力されます。

## データセットの追加

`settings.yml` を編集し、以下を実行してください。

```
python 300_create_batch.py
```
`201_batches.sh` が更新されます。

