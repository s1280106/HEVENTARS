# Area.py

"""
指定された標高タイルから標高を取得し、計算範囲の調整を行うモジュールです。
This module obtains the elevation from the specified elevation tile and adjusts the calculation range.
"""

import os
import numpy as np
import tifffile
import math

# 標高データを取得
def get_elevation(img_path, LINE_SAMPLES, LINES):
    """
    Args:
    img_path: 標高データのパス
    LINES_SAMPLES, LINES: データサイズ
    
    Return:
    elevation_data: 標高データ
    """
    
    print("標高データ構築中...")
    
    data = np.fromfile(img_path, dtype=">i2")
    elevation_data = data.reshape(LINES, LINE_SAMPLES)
    return elevation_data


# 対象を中心として特定範囲の標高データを抽出する
def select_area(elevation_data, target_latitude, target_longitude, LINE_SAMPLES, LINES,
                UPPER_LEFT_LATITUDE, UPPER_LEFT_LONGITUDE, MAP_RESOLUTION, plot_range):
    """
    Args:
    elevation_data: 標高データ
    target_latitude: 対象の緯度
    target_longitude: 対象の経度
    LINE_SAMPLES, LINES: データサイズ
    UPPER_LEFT_LATITUDE, UPPER_LEFT_LONGITUDE: タイル左上の緯度経度
    MAP_RESOLUTION: マップスケーリング係数 <km/pixel>
    plot_range: プロット管理番号

    Returns:
    selected_data: 抽出された標高データ
    selected_x: 抽出されたピクセルの経度データ
    selected_y: 抽出されたピクセルの緯度データ
    haversine_data: 曲率補正された標高データ
    """
    
    print("標高データ整形中...")
    
    # 第1段階 ピクセル座標を緯度と経度に変換
    lon = UPPER_LEFT_LONGITUDE + np.arange(LINE_SAMPLES) / MAP_RESOLUTION
    lat = UPPER_LEFT_LATITUDE - np.arange(LINES) / MAP_RESOLUTION
    x, y = np.meshgrid(lon, lat)
    
    # 第2段階 管理番号に基づいて抽出範囲を指定
    if plot_range == 0:   # range: 6,000m
        plot_range = 0.1    # <deg>
    elif plot_range == 1: # range: 3,000m
        plot_range = 0.05   # <deg>
    elif plot_range == 2: # range: 600m
        plot_range = 0.01   # <deg>
    else:                 # range: 300m
        plot_range = 0.005  # <deg>

    # 通常の抽出（変更の必要なければこのまま）
    x_indices = np.where((lon >= target_longitude - plot_range) & (lon <= target_longitude + plot_range))[0]
    y_indices = np.where((lat >= target_latitude - plot_range) & (lat <= target_latitude + plot_range))[0]
    
    # 抽出範囲を変化させる場合はコチラ
    # Plot.py のアスペクト比の変更をあわせて推奨します。
    #x_indices = np.where((lon >= target_longitude - (plot_range)) & (lon <= target_longitude + (plot_range)))[0]
    #y_indices = np.where((lat >= target_latitude - plot_range*10) & (lat <= target_latitude + 0))[0]
    
    # 第3段階 範囲内のデータを抽出
    selected_x = x[y_indices[:, np.newaxis], x_indices]
    selected_y = y[y_indices[:, np.newaxis], x_indices]
    selected_data = elevation_data[y_indices[:, np.newaxis], x_indices]
    
    print("曲率補正中...")
    
    # 第4段階 曲率による標高補正
    haversine_data = np.array([haversine_distance(elevation, LAT, LON, target_latitude, target_longitude)
                            for elevation, LAT, LON in zip(selected_data.flatten(), selected_y.flatten(), selected_x.flatten())])
    haversine_data = haversine_data.reshape(selected_data.shape)
    
    # データ間隔を調整する場合（結果のファイルサイズが大きくなりすぎる場合）
    # データを1つ飛ばしで再調整する
    """
    haversine_data = haversine_data[::2, ::2]
    selected_data = selected_data[::2, ::2]
    selected_x = selected_x[::2, ::2]
    selected_y = selected_y[::2, ::2]
    """
    return selected_data, selected_x, selected_y, haversine_data


# LRO: 標高データを取得
def get_elevation_LRO(tif_name):
    """
    Arg:
    tif_name: ファイル名
    
    Return:
    elevation_data: 標高データ
    """
    
    print("標高データ構築中...")
    
    # データにアクセス
    script_directory = os.path.dirname(os.path.abspath(__file__))
    elevation_file_path = os.path.join(script_directory, "..", "data", tif_name)
    # tifffileで読み込む
    data = tifffile.imread(elevation_file_path)
    # エンディアン変換（ビッグエンディアンからリトルエンディアンへ）
    data_endian = data.byteswap().newbyteorder()
    # float 32 に変換
    elevation_data = data_endian.astype('float32')
    return elevation_data


# 標高データの曲率補正
# 参考サイト： https://qiita.com/port-development/items/eea3a0a225be47db0fd4
# 参考サイト： https://manabitimes.jp/math/1233
def haversine_distance(elevation, LAT, LON, target_latitude, target_longitude):
    """
    Args:
    elevation: 計算対象の標高
    LAT: 計算対象の緯度
    LON: 計算対象の経度
    target_latitude: ターゲット地点の緯度
    target_longitude: ターゲット地点の経度
    
    Return: 
    haversine_elevation: 曲率補正後の標高
    """

    # 月の半径 <m>
    R = 1737400
    # ラジアン変換
    rad = math.pi/180
    LAT, LON, target_LAT, target_LON = LAT*rad, LON*rad, target_latitude*rad, target_longitude*rad
    # 三角関数定義
    acos, sin, cos = math.acos, math.sin, math.cos
    # 2点間の経度差
    LON_diff = abs(LON-target_LON)
    # 2点間と月中心で構成される角度を求める
    theta = acos(sin(LAT)*sin(target_LAT) + cos(LAT)*cos(target_LAT)*cos(LON_diff))
    # 標高差を求める <m>
    h = R/cos(theta) - R
    # 曲率補正を適応する
    haversine_elevation = elevation - h
    
    return haversine_elevation