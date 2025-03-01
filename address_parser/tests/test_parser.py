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
    assert parser.extract_prefecture("東京都新宿区西新宿1-2-3") == "東京都"
    assert parser.extract_prefecture("大阪府大阪市北区梅田1-2-3") == "大阪府"
    assert parser.extract_prefecture("京都府京都市中京区烏丸通1-2-3") == "京都府"
    assert parser.extract_prefecture("北海道札幌市中央区北1条西2-3-4") == "北海道"


def test_extract_prefecture_abbreviated():
    """
    省略形の都道府県表記のテスト
    """
    parser = AddressParser()
    
    # 省略形の都道府県表記
    assert parser.extract_prefecture("東京新宿区西新宿1-2-3") == "東京都"
    assert parser.extract_prefecture("大阪大阪市北区梅田1-2-3") == "大阪府"
    assert parser.extract_prefecture("京都京都市中京区烏丸通1-2-3") == "京都府"


def test_extract_prefecture_not_found():
    """
    都道府県名が含まれない住所のテスト
    """
    parser = AddressParser()
    
    # 都道府県名が含まれない住所
    assert parser.extract_prefecture("新宿区西新宿1-2-3") == ""
    assert parser.extract_prefecture("") == ""


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