# 日本語住所正規化ツール

日本語の住所文字列を解析し、都道府県、市区町村、町名番地、その他の要素（建物名・部屋番号など）に分割するPythonライブラリです。

## 特徴

- 日本語の住所文字列を構造化されたデータに変換
- 都道府県、市区町村、町名番地、その他の要素（建物名・部屋番号など）に分割
- 全角数字・記号の半角変換
- 漢数字の数字変換
- 政令指定都市の特別区の処理
- 様々な住所形式に対応

## インストール

```bash
pip install -r requirements.txt
```

## 使い方

```python
from address_parser.parser import AddressParser

# パーサーの初期化
parser = AddressParser()

# 住所の解析
result = parser.parse_address("東京都新宿区西新宿1-2-3 〇〇ビル101号室")
print(result)
# 出力: {'prefecture': '東京都', 'city': '新宿区', 'town_street': '西新宿1-2-3', 'other': '〇〇ビル101号室'}

# 全角数字を含む住所の解析
result = parser.parse_address("東京都新宿区西新宿１－２－３")
print(result)
# 出力: {'prefecture': '東京都', 'city': '新宿区', 'town_street': '西新宿1-2-3', 'other': ''}

# 漢数字を含む住所の解析
result = parser.parse_address("東京都新宿区西新宿一丁目二番三号")
print(result)
# 出力: {'prefecture': '東京都', 'city': '新宿区', 'town_street': '西新宿1丁目2番3号', 'other': ''}
```

## 対応している住所形式

- 標準的な住所形式: `東京都新宿区西新宿1-2-3`
- 郵便番号付き: `〒123-4567 東京都新宿区西新宿1-2-3`
- 建物名・部屋番号付き: `東京都新宿区西新宿1-2-3 〇〇ビル101号室`
- 漢数字表記: `東京都新宿区西新宿一丁目二番三号`
- 全角数字・記号: `東京都新宿区西新宿１－２－３`
- 政令指定都市の特別区: `大阪府大阪市北区梅田1-2-3`
- 郡を含む町村: `北海道河東郡音更町木野西通1-2-3`

## テスト

```bash
python -m pytest
```

## ライセンス

MIT

## 作者

[Your Name] 