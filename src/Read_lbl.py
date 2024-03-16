# Rear_lbl.py

"""
ダウンロードしたlblファイルから情報を取得して返すモジュールです。
This module returns information from a downloaded lbl file.
"""

import os
import re

# lblファイルから特定の値を読み取る
def get_lbl(file_path, target_keys):
    """
    Args:
    file_path: 対象のlblファイルのパス
    target_keys: 読み取る単語の辞書
    
    Return:
    topographic_info: 結果値の辞書
    """
    
    print("地理情報の読み取り中...")
    
    # ファイルが存在するか確認
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    # ファイルを読み込む
    with open(file_path, 'r') as file:
        # ファイルの内容を取得
        lbl_content = file.read()
        
    # 結果を格納
    topographic_info = {}

    for target_key in target_keys:
        # 正規表現パターンを構築
        pattern = re.compile(rf'{target_key}\s*=\s*([-+]?\d*\.\d+|\d+)')

        # ファイルの各行を検査
        for line in lbl_content.split('\n'):
            match = pattern.search(line)
            if match:
                # 一致した行から数値を抽出して辞書に追加
                topographic_info[target_key] = float(match.group(1))
                break

    return topographic_info
