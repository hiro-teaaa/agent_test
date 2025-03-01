"""
日本語住所を解析するためのモジュール
"""
import re


class AddressParser:
    """
    日本語の住所文字列を解析し、構造化されたデータに変換するクラス
    """

    def __init__(self):
        """
        AddressParserクラスの初期化
        """
        # 都道府県リスト
        self.prefectures = [
            "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
            "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
            "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
            "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
            "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
            "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
            "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
        ]
        
        # 都道府県の省略形マッピング
        self.prefecture_aliases = {
            "東京": "東京都",
            "大阪": "大阪府",
            "京都": "京都府",
            # 他の省略形も必要に応じて追加
        }
        
        # 市区町村の接尾辞パターン
        self.city_suffixes = ["市", "区", "町", "村"]
        
        # 政令指定都市のリスト
        self.designated_cities = [
            "札幌市", "仙台市", "さいたま市", "千葉市", "横浜市", "川崎市", "相模原市",
            "新潟市", "静岡市", "浜松市", "名古屋市", "京都市", "大阪市", "堺市",
            "神戸市", "岡山市", "広島市", "北九州市", "福岡市", "熊本市"
        ]
        
        # 数字の漢数字変換マッピング
        self.kanji_numbers = {
            "一": "1", "二": "2", "三": "3", "四": "4", "五": "5",
            "六": "6", "七": "7", "八": "8", "九": "9", "十": "10"
        }

    def parse_address(self, address_string):
        """
        住所文字列を解析して構造化データを返す

        Args:
            address_string (str): 解析する住所文字列

        Returns:
            dict: 解析された住所の構造化データ
                {
                    "prefecture": "都道府県名",
                    "city": "市区町村名",
                    "town_street": "町名番地",
                    "other": "建物名・部屋番号など"
                }
        """
        # 郵便番号を除去（あれば）
        address_string = re.sub(r'〒\d{3}-\d{4}', '', address_string).strip()
        
        # 都道府県を抽出
        prefecture = self.extract_prefecture(address_string)
        
        # 都道府県を除去した残りの住所
        remaining_address = address_string
        if prefecture:
            remaining_address = address_string[len(prefecture):].strip()
        
        # 市区町村を抽出
        city = self.extract_city(remaining_address, prefecture)
        
        # 市区町村を除去した残りの住所
        remaining_address = remaining_address
        if city:
            remaining_address = remaining_address[len(city):].strip()
        
        # 町名番地を抽出
        town_street = self.extract_town_street(remaining_address, prefecture, city)
        
        return {
            "prefecture": prefecture,
            "city": city,
            "town_street": town_street,
            "other": ""
        }

    def extract_prefecture(self, address_string):
        """
        住所文字列から都道府県を抽出する

        Args:
            address_string (str): 解析する住所文字列

        Returns:
            str: 抽出された都道府県名
        """
        # 完全一致の都道府県名を検索
        for prefecture in self.prefectures:
            if address_string.startswith(prefecture):
                return prefecture
        
        # 省略形の都道府県名を検索
        for alias, full_name in self.prefecture_aliases.items():
            if address_string.startswith(alias):
                return full_name
        
        # 都道府県名が見つからない場合は空文字列を返す
        return ""

    def extract_city(self, address_string, prefecture):
        """
        住所文字列から市区町村を抽出する

        Args:
            address_string (str): 解析する住所文字列
            prefecture (str): 抽出された都道府県名

        Returns:
            str: 抽出された市区町村名
        """
        if not address_string:
            return ""
        
        # 政令指定都市の特別区を処理
        for city in self.designated_cities:
            if address_string.startswith(city):
                # 政令指定都市の後に区がある場合（例: 大阪市北区）
                district_match = re.match(f"{city}(.+?区)", address_string)
                if district_match:
                    return f"{city}{district_match.group(1)}"
                return city
        
        # 一般的な市区町村の抽出パターン
        city_match = re.match(r'(.+?[市区町村])', address_string)
        if city_match:
            return city_match.group(1)
        
        # 特殊なケース: 郡を含む町村（例: ○○郡△△町）
        gun_match = re.match(r'(.+?郡.+?[町村])', address_string)
        if gun_match:
            return gun_match.group(1)
        
        return ""

    def extract_town_street(self, address_string, prefecture, city):
        """
        住所文字列から町名番地を抽出する

        Args:
            address_string (str): 解析する住所文字列
            prefecture (str): 抽出された都道府県名
            city (str): 抽出された市区町村名

        Returns:
            str: 抽出された町名番地
        """
        if not address_string:
            return ""
        
        # 建物名や部屋番号を分離するパターン
        # 一般的には番地の後にスペースがあり、その後に建物名が続く
        parts = address_string.split(" ", 1)
        town_street_part = parts[0]
        
        # 数字とハイフンを含む番地パターンを検出
        # 例: 西新宿1-2-3
        number_pattern = re.search(r'([^\d]+)([\d-]+.*?)$', town_street_part)
        if number_pattern:
            return town_street_part
        
        # 漢数字を含む番地パターンを検出
        # 例: 西新宿一丁目二番三号
        kanji_pattern = re.search(r'(.+?[町])(.+?[丁目])(.+?[番])(.+?[号])', town_street_part)
        if kanji_pattern:
            return town_street_part
        
        # 番地がない場合は町名のみを返す
        return town_street_part

    def extract_other(self, address_string, prefecture, city, town_street):
        """
        住所文字列からその他の要素（建物名・部屋番号など）を抽出する

        Args:
            address_string (str): 解析する住所文字列
            prefecture (str): 抽出された都道府県名
            city (str): 抽出された市区町村名
            town_street (str): 抽出された町名番地

        Returns:
            str: 抽出されたその他の要素
        """
        # 後で実装
        return ""

    def normalize_address(self, address_dict):
        """
        抽出した住所を正規化する

        Args:
            address_dict (dict): 解析された住所の構造化データ

        Returns:
            dict: 正規化された住所の構造化データ
        """
        # 後で実装
        return address_dict 