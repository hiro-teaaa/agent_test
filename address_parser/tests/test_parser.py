"""
AddressParserクラスのテスト
"""

import pytest
from address_parser.parser import AddressParser


def test_address_parser_initialization():
    """
    AddressParserクラスが正しく初期化されることをテスト
    """
    parser = AddressParser()
    assert isinstance(parser, AddressParser)
    assert isinstance(parser.prefectures, list)
    assert len(parser.prefectures) == 47  # 47都道府県


def test_parse_address_method():
    """
    parse_addressメソッドが呼び出せることをテスト
    """
    parser = AddressParser()
    result = parser.parse_address("東京都新宿区西新宿1-2-3")
    
    assert isinstance(result, dict)
    assert "prefecture" in result
    assert "city" in result
    assert "town_street" in result
    assert "other" in result


def test_extract_prefecture_standard():
    """
    標準的な都道府県表記のテスト
    """
    parser = AddressParser()
    
    # 標準的な都道府県表記
    assert parser.extract_prefecture("東京都新宿区西新宿1-2-3")[0] == "東京都"
    assert parser.extract_prefecture("大阪府大阪市北区梅田1-2-3")[0] == "大阪府"
    assert parser.extract_prefecture("京都府京都市中京区烏丸通1-2-3")[0] == "京都府"
    assert parser.extract_prefecture("北海道札幌市中央区北1条西2-3-4")[0] == "北海道"


def test_extract_prefecture_abbreviated():
    """
    省略形の都道府県表記のテスト
    """
    parser = AddressParser()
    
    # 省略形の都道府県表記
    result = parser.extract_prefecture("東京新宿区西新宿1-2-3")
    assert result[0] == "東京都"
    assert result[1] == "東京"
    
    result = parser.extract_prefecture("大阪大阪市北区梅田1-2-3")
    assert result[0] == "大阪府"
    assert result[1] == "大阪"
    
    result = parser.extract_prefecture("京都京都市中京区烏丸通1-2-3")
    assert result[0] == "京都府"
    assert result[1] == "京都"


def test_extract_prefecture_not_found():
    """
    都道府県名が含まれない住所のテスト
    """
    parser = AddressParser()
    
    # 都道府県名が含まれない住所
    assert parser.extract_prefecture("新宿区西新宿1-2-3")[0] == ""
    assert parser.extract_prefecture("")[0] == ""


def test_extract_city_standard():
    """
    標準的な市区町村表記のテスト
    """
    parser = AddressParser()
    
    # 標準的な市区町村表記
    assert parser.extract_city("新宿区西新宿1-2-3", "東京都") == "新宿区"
    assert parser.extract_city("大阪市北区梅田1-2-3", "大阪府") == "大阪市北区"  # 注意: 実際には「大阪市」と「北区」に分けるべき
    assert parser.extract_city("京都市中京区烏丸通1-2-3", "京都府") == "京都市中京区"  # 注意: 実際には「京都市」と「中京区」に分けるべき
    assert parser.extract_city("中央区北1条西2-3-4", "北海道") == "中央区"


def test_extract_city_special():
    """
    特殊な市区町村表記のテスト
    """
    parser = AddressParser()
    
    # 特殊な市区町村表記
    assert parser.extract_city("府中市宮西町1-2-3", "東京都") == "府中市"
    assert parser.extract_city("郡山市開成1-2-3", "福島県") == "郡山市"
    
    # 郡を含む町村
    assert parser.extract_city("河東郡音更町木野西通1-2-3", "北海道") == "河東郡音更町"


def test_extract_city_not_found():
    """
    市区町村名が含まれない住所のテスト
    """
    parser = AddressParser()
    
    # 市区町村名が含まれない住所
    assert parser.extract_city("", "東京都") == ""
    assert parser.extract_city("西新宿1-2-3", "東京都") == ""  # 市区町村名がない場合


def test_extract_town_street_standard():
    """
    標準的な町名番地表記のテスト
    """
    parser = AddressParser()
    
    # 標準的な町名番地表記
    assert parser.extract_town_street("西新宿1-2-3", "東京都", "新宿区") == "西新宿1-2-3"
    assert parser.extract_town_street("梅田1-2-3", "大阪府", "大阪市北区") == "梅田1-2-3"
    assert parser.extract_town_street("烏丸通1-2-3", "京都府", "京都市中京区") == "烏丸通1-2-3"


def test_extract_town_street_kanji():
    """
    漢字表記の番地のテスト
    """
    parser = AddressParser()
    
    # 漢字表記の番地
    assert parser.extract_town_street("西新宿一丁目二番三号", "東京都", "新宿区") == "西新宿一丁目二番三号"
    assert parser.extract_town_street("本町一丁目", "大阪府", "大阪市中央区") == "本町一丁目"


def test_extract_town_street_no_number():
    """
    番地がない町名のみの住所のテスト
    """
    parser = AddressParser()
    
    # 番地がない町名のみ
    assert parser.extract_town_street("西新宿", "東京都", "新宿区") == "西新宿"
    assert parser.extract_town_street("梅田", "大阪府", "大阪市北区") == "梅田"


def test_extract_town_street_with_building():
    """
    建物名を含む町名番地のテスト
    """
    parser = AddressParser()
    
    # 建物名を含む町名番地（スペースで区切られている場合）
    assert parser.extract_town_street("西新宿1-2-3 〇〇ビル101", "東京都", "新宿区") == "西新宿1-2-3"


def test_extract_other_building():
    """
    建物名のテスト
    """
    parser = AddressParser()
    
    # 建物名のみ
    assert parser.extract_other("〇〇ビル", "東京都", "新宿区", "西新宿1-2-3") == "〇〇ビル"
    assert parser.extract_other("〇〇マンション", "大阪府", "大阪市北区", "梅田1-2-3") == "〇〇マンション"


def test_extract_other_room():
    """
    部屋番号のテスト
    """
    parser = AddressParser()
    
    # 部屋番号のみ
    assert parser.extract_other("101号室", "東京都", "新宿区", "西新宿1-2-3") == "101号室"
    assert parser.extract_other("202室", "大阪府", "大阪市北区", "梅田1-2-3") == "202室"


def test_extract_other_building_and_room():
    """
    建物名と部屋番号の組み合わせのテスト
    """
    parser = AddressParser()
    
    # 建物名と部屋番号の組み合わせ
    assert parser.extract_other("〇〇ビル101号室", "東京都", "新宿区", "西新宿1-2-3") == "〇〇ビル101号室"
    assert parser.extract_other("〇〇マンション 202室", "大阪府", "大阪市北区", "梅田1-2-3") == "〇〇マンション 202室"


def test_extract_other_not_found():
    """
    その他の要素がない場合のテスト
    """
    parser = AddressParser()
    
    # その他の要素がない場合
    assert parser.extract_other("", "東京都", "新宿区", "西新宿1-2-3") == ""


def test_normalize_address_zenkaku_numbers():
    """
    全角数字を含む住所の正規化テスト
    """
    parser = AddressParser()
    
    # 全角数字を含む住所
    result = parser.parse_address("東京都新宿区西新宿１－２－３")
    assert result["town_street"] == "西新宿1-2-3"


def test_normalize_address_kanji_numbers():
    """
    漢数字を含む住所の正規化テスト
    """
    parser = AddressParser()
    
    # 漢数字を含む住所
    result = parser.parse_address("東京都新宿区西新宿一丁目二番三号")
    assert result["town_street"] == "西新宿1丁目2番3号"


def test_normalize_address_symbols():
    """
    全角記号を含む住所の正規化テスト
    """
    parser = AddressParser()
    
    # 全角記号を含む住所
    result = parser.parse_address("東京都新宿区西新宿１－２－３　〇〇ビル１０１号室")
    assert result["town_street"] == "西新宿1-2-3"
    assert result["other"] == "〇〇ビル101号室"


def test_parse_address_with_abbreviated_prefecture():
    """
    省略形の都道府県名を含む住所の解析テスト
    """
    parser = AddressParser()
    
    # 省略形の都道府県名を含む住所
    result = parser.parse_address("東京新宿区西新宿1-2-3")
    assert result["prefecture"] == "東京都"
    assert result["city"] == "新宿区"
    assert result["town_street"] == "西新宿1-2-3"
    assert result["other"] == ""
    
    result = parser.parse_address("大阪大阪市北区梅田1-2-3")
    assert result["prefecture"] == "大阪府"
    assert result["city"] == "大阪市北区"
    assert result["town_street"] == "梅田1-2-3"
    assert result["other"] == ""
    
    result = parser.parse_address("京都京都市中京区烏丸通1-2-3")
    assert result["prefecture"] == "京都府"
    assert result["city"] == "京都市中京区"
    assert result["town_street"] == "烏丸通1-2-3"
    assert result["other"] == ""


def test_prefecture_name_appears_twice():
    """
    都道府県名が2回登場する住所のテスト
    例: 長野県長野市南長野県町477-1
    """
    parser = AddressParser()
    
    # 都道府県名が2回登場する住所
    result = parser.parse_address("長野県長野市南長野県町477-1")
    
    assert result["prefecture"] == "長野県"
    assert result["city"] == "長野市"
    assert result["town_street"] == "南長野県町477-1"
    assert result["other"] == ""


def test_chome_directly_under_city():
    """
    市区町村直下に丁目が存在する住所のテスト
    例: 静岡県下田市2丁目4-26
    """
    parser = AddressParser()
    
    # 市区町村直下に丁目が存在する住所
    result = parser.parse_address("静岡県下田市2丁目4-26")
    
    assert result["prefecture"] == "静岡県"
    assert result["city"] == "下田市"
    assert result["town_street"] == "2丁目4-26"
    assert result["other"] == ""


def test_town_name_with_number():
    """
    町名に数字が含まれる住所のテスト
    例: 埼玉県春日部市八丁目123
    """
    parser = AddressParser()
    
    # 町名に数字が含まれる住所
    result = parser.parse_address("埼玉県春日部市八丁目123")
    
    assert result["prefecture"] == "埼玉県"
    assert result["city"] == "春日部市"
    # 漢数字「八」は正規化処理で「8」に変換される
    assert result["town_street"] == "8丁目123"
    assert result["other"] == ""


def test_address_with_oaza_koaza():
    """
    大字・小字を含む住所のテスト
    例: 島根県出雲市大社町杵築東宮内195
    """
    parser = AddressParser()
    
    # 大字・小字を含む住所
    result = parser.parse_address("島根県出雲市大社町杵築東宮内195")
    
    assert result["prefecture"] == "島根県"
    assert result["city"] == "出雲市"
    assert result["town_street"] == "大社町杵築東宮内195"
    assert result["other"] == ""


def test_address_with_street_name_kyoto():
    """
    通り名を用いた住所（京都市の例）のテスト
    例: 京都府京都市中京区寺町通御池上ル上本能寺前町488
    """
    parser = AddressParser()
    
    # 通り名を用いた住所
    result = parser.parse_address("京都府京都市中京区寺町通御池上ル上本能寺前町488")
    
    assert result["prefecture"] == "京都府"
    assert result["city"] == "京都市中京区"
    assert result["town_street"] == "寺町通御池上ル上本能寺前町488"
    assert result["other"] == ""


def test_address_with_grid_pattern_sapporo():
    """
    碁盤の目状の住所（札幌市の例）のテスト
    例: 北海道札幌市中央区北1条西2丁目5番地
    """
    parser = AddressParser()
    
    # 碁盤の目状の住所
    result = parser.parse_address("北海道札幌市中央区北1条西2丁目5番地")
    
    assert result["prefecture"] == "北海道"
    assert result["city"] == "札幌市中央区"
    assert result["town_street"] == "北1条西2丁目5番地"
    assert result["other"] == "" 