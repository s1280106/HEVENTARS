# Download.py

"""
生成されたタイル名をもとに該当する2つのファイル(標高データとラベルファイル)をダウンロードし、ファイルパスを返すモジュールです。
This module downloads the two corresponding files (elevation data and label file) based on the generated tile names and returns the file paths.
"""

import os
import requests
import sys

# 対象のファイルをダウンロードする
def download_data(prefix, name):
    """
    Args:
    prefix: 経度の分類
    name: タイルの名前
    
    Returns:
    img_filename: imgファイルの名前
    lbl_filename: lblファイルの名前
    """
    
    # URLの構築
    base_url = f'https://data.darts.isas.jaxa.jp/pub/pds3/sln-l-tc-5-dtm-map-seamless-v2.0/{prefix}/data/'
    img_url = base_url + f'DTM_MAPs02_{name}SC.img'
    lbl_url = base_url + f'DTM_MAPs02_{name}SC.lbl'
    
    # 保存先の設定
    script_directory = os.path.dirname(os.path.abspath(__file__))
    save_directory = os.path.join(script_directory, "..", "data")

    # ダウンロードするファイル名を指定
    img_filename = os.path.join(save_directory, f'DTM_MAPs02_{name}SC.img')
    lbl_filename = os.path.join(save_directory, f'DTM_MAPs02_{name}SC.lbl')
    
    # すでにファイルが存在する場合はダウンロードを中止して、続行
    if os.path.exists(img_filename) or os.path.exists(lbl_filename):
        print(f'[{img_filename}] or [{lbl_filename}] already exists. Abort download.')
        return img_filename, lbl_filename

    try:
        # imgをダウンロード
        img_response = requests.get(img_url)
        with open(img_filename, 'wb') as img_file:
            img_file.write(img_response.content)
        print(f'{img_filename} ダウンロード成功')

        # lblをダウンロード
        lbl_response = requests.get(lbl_url)
        with open(lbl_filename, 'wb') as lbl_file:
            lbl_file.write(lbl_response.content)
        print(f'{lbl_filename} ダウンロード成功')
        
        # ダウンロードしたファイルのパスを返す
        return img_filename, lbl_filename

    except requests.RequestException as e:
        print(f'Error: {e}')
        # エラーが発生した場合、プログラムを終了
        sys.exit()

# 対象のオルソをダウンロードする
def download_ortho(prefix, name):
    """
    Args:
    prefix: 経度の分類
    name: タイルの名前
    
    Returns:
    img_filename: imgファイルの名前
    lbl_filename: lblファイルの名前
    """
    
    # URLの構築
    base_url = f'https://data.darts.isas.jaxa.jp/pub/pds3/sln-l-tc-5-ortho-map-seamless-v2.0/{prefix}/data/'
    img_url = base_url + f'TCO_MAPs02_{name}SC.img'
    lbl_url = base_url + f'TCO_MAPs02_{name}SC.lbl'
    
    # 保存先の設定
    script_directory = os.path.dirname(os.path.abspath(__file__))
    save_directory = os.path.join(script_directory, "..", "data")

    # ダウンロードするファイル名を指定
    img_filename = os.path.join(save_directory, f'TCO_MAPs02_{name}SC.img')
    lbl_filename = os.path.join(save_directory, f'TCO_MAPs02_{name}SC.lbl')
    
    # すでにファイルが存在する場合はダウンロードを中止して、続行
    if os.path.exists(img_filename) or os.path.exists(lbl_filename):
        print(f'[{img_filename}] or [{lbl_filename}] already exists. Abort download.')
        return img_filename, lbl_filename

    try:
        # imgをダウンロード
        img_response = requests.get(img_url)
        with open(img_filename, 'wb') as img_file:
            img_file.write(img_response.content)
        print(f'{img_filename} ダウンロード成功')

        # lblをダウンロード
        lbl_response = requests.get(lbl_url)
        with open(lbl_filename, 'wb') as lbl_file:
            lbl_file.write(lbl_response.content)
        print(f'{lbl_filename} ダウンロード成功')
        
        # ダウンロードしたファイルのパスを返す
        return img_filename, lbl_filename

    except requests.RequestException as e:
        print(f'Error: {e}')
        # エラーが発生した場合、プログラムを終了
        sys.exit()