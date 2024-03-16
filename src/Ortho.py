# Ortho.py

"""
指定されたオルソ画像タイルを取得し、抽出範囲の調整を行うモジュールです。
This module obtains the elevation from the specified elevation tile and adjusts the calculation range.
"""

import os
import numpy as np

def get_ortho(ortho_img_path, LINES, LINE_SAMPLES):
    """
    Args:
    img_path: オルソ画像のパス
    LINES_SAMPLES, LINES: データサイズ
    
    Return:
    ortho_image: オルソ画像 
    """
    
    print("オルソ画像の読み込み中...")
    
    # バイナリモードでファイルを開く
    with open(ortho_img_path, 'rb') as file:
        # NumPyで画像を読み込み
        image_array = np.fromfile(file, dtype=">u2")
        ortho_image = image_array.reshape(LINES, LINE_SAMPLES)
    return ortho_image


# 対象を中心として特定範囲のオルソ画像を抽出する
def selected_ortho(ortho_image, target_latitude, target_longitude, LINE_SAMPLES, LINES,
                UPPER_LEFT_LATITUDE, UPPER_LEFT_LONGITUDE, MAP_RESOLUTION, plot_range):
    """
    Args:
    ortho_image: オルソ画像
    target_latitude: 対象の緯度
    target_longitude: 対象の経度
    LINE_SAMPLES, LINES: データサイズ
    UPPER_LEFT_LATITUDE, UPPER_LEFT_LONGITUDE: タイル左上の緯度経度
    MAP_RESOLUTION: マップスケーリング係数 <km/pixel>
    plot_range: プロット管理番号

    Return:
    selected_ortho: 抽出されたオルソ画像
    """
    
    print("オルソ画像整形中...")
    
    # 第1段階 ピクセル座標を緯度と経度に変換
    lon = UPPER_LEFT_LONGITUDE + np.arange(LINE_SAMPLES) / MAP_RESOLUTION
    lat = UPPER_LEFT_LATITUDE - np.arange(LINES) / MAP_RESOLUTION
    
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
    # 現在の記述： 経度の範囲を東西に半減、緯度の範囲を北方向に限定
    #x_indices = np.where((lon >= target_longitude - (plot_range/2)) & (lon <= target_longitude + (plot_range/2)))[0]
    #y_indices = np.where((lat >= target_latitude - 0) & (lat <= target_latitude + plot_range))[0]
    
    # 第3段階 範囲内のデータを抽出
    selected_ortho = ortho_image[y_indices[:, np.newaxis], x_indices]
    
    return selected_ortho