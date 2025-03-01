#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日本語住所正規化ツールの使用例
"""

from address_parser.parser import AddressParser


def main():
    """
    メイン関数
    """
    # パーサーの初期化
    parser = AddressParser()
    
    # テスト用の住所リスト
    addresses = [
        "東京都新宿区西新宿1-2-3",
        "〒123-4567 東京都新宿区西新宿1-2-3",
        "東京都新宿区西新宿1-2-3 〇〇ビル101号室",
        "東京都新宿区西新宿一丁目二番三号",
        "東京都新宿区西新宿１－２－３",
        "大阪府大阪市北区梅田1-2-3",
        "北海道河東郡音更町木野西通1-2-3",
        "新宿区西新宿1-2-3",  # 都道府県名なし
        "東京新宿区西新宿1-2-3",  # 都道府県名の省略
        "東京都 新宿区 西新宿 1-2-3",  # スペース区切り
        "東京都新宿区西新宿",  # 番地なし
    ]
    
    # 各住所を解析して結果を表示
    for address in addresses:
        result = parser.parse_address(address)
        print(f"入力: {address}")
        print(f"結果: {result}")
        print("---")


if __name__ == "__main__":
    main() 