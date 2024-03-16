# Save.py

"""
3Dプロットデータを保存し、展開するモジュールです。
This module saves and expands 3D plot data.
"""

import os
import webbrowser

def save_expand(fig, target_latitude, target_longitude, 
                sun_azimuth, sun_altdeg, smoothing_active, ortho_active, plot_range):
    """
    Args:
    fig: 3Dプロット
    target_latitude: ターゲットの緯度
    target_longitude: ターゲットの経度
    sun_azimuth: 太陽（光源）の方位
    sun_altdeg: 太陽（光源の仰角）
    smoothing_active: スムージング機能の有効化
    ortho_active: オルソ画像の使用
    plot_range: プロット管理番号
    
    Return:
    None
    """
    
    print("プロットの保存中...")
    
    # 保存先の設定
    save_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "result")
    
    # 緯度経度のシンボル設定
    lat_symbol = "S" if target_latitude < 0 else "N"
    lon_symbol = "E"
    
    # 各引数の表記整理
    # 小数点以下５桁に丸め、整数に直す
    target_latitude = int(abs(round(target_latitude, 5) * pow(10, 5)))
    target_longitude = int(abs(round(target_longitude, 5) * pow(10, 5)))
    sun_azimuth = int(round(sun_azimuth, 5) * pow(10, 5))
    sun_altdeg = int(round(sun_altdeg, 5) * pow(10, 5))
    
    # ファイル名の設定
    
    # スムージングが無効の場合
    if smoothing_active == False:
        if ortho_active == False:
            # スムージングなし、陰影起伏
            sava_option = "HVTS_SIM_h_KGY_"
        else:
            # スムージングなし、オルソ画像
            sava_option = "HVTS_SIM_o_KGY_"
    # スムージングが有効の場合
    else:
        if ortho_active == False:
            # スムージングあり、陰影起伏
            sava_option = "HVTS_SIMs_h_KGY_"
        else:
            # スムージングあり、オルソ画像
            sava_option = "HVTS_SIMs_o_KGY_"
    
    # プロット範囲のシンボル設定
    if plot_range == 0:
        plot_symbol = "60_"
    elif plot_range == 1:
        plot_symbol = "30_"
    elif plot_range == 2:
        plot_symbol = "06_"
    else:
        plot_symbol = "03_"
    
    # 保存ファイル名の設定
    save_name = sava_option + plot_symbol + f"{lat_symbol}{target_latitude:07}{lon_symbol}{target_longitude:08}_azim{sun_azimuth:08}alt{sun_altdeg:07}.html"
    save_filename = os.path.join(save_directory, save_name)
    
    # 3Dプロットの保存
    fig.write_html(save_filename)
    # プロット表示
    webbrowser.open('file:///' + save_filename, new=2)
    

def save_expand_LRO(fig, target_latitude, target_longitude, 
                sun_azimuth, sun_altdeg, smoothing_active, plot_range):
    """
    Args:
    fig: 3Dプロット
    target_latitude: ターゲットの緯度
    target_longitude: ターゲットの経度
    sun_azimuth: 太陽（光源）の方位
    sun_altdeg: 太陽（光源の仰角）
    smoothing_active: スムージング機能の有効化
    plot_range: プロット管理番号
    
    Return:
    None
    """
    
    print("プロットの保存中...")
    
    # 保存先の設定
    save_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "result")
    
    # 緯度経度のシンボル設定
    lat_symbol = "S" if target_latitude < 0 else "N"
    lon_symbol = "E"
    
    # 各引数の表記整理
    # 小数点以下５桁に丸め、整数に直す
    target_latitude = int(abs(round(target_latitude, 5) * pow(10, 5)))
    target_longitude = int(abs(round(target_longitude, 5) * pow(10, 5)))
    sun_azimuth = int(round(sun_azimuth, 5) * pow(10, 5))
    sun_altdeg = int(round(sun_altdeg, 5) * pow(10, 5))
    
    # スムージングが有効の場合
    if smoothing_active == True:
        sava_option = "HVTS_SIMs_LRO_"
    else:
        sava_option = "HVTS_SIM_LRO_"
        
    # プロット範囲のシンボル設定
    if plot_range == 0:
        plot_symbol = "60_"
    elif plot_range == 1:
        plot_symbol = "30_"
    elif plot_range == 2:
        plot_symbol = "06_"
    else:
        plot_symbol = "03_"
    
    # 保存ファイル名の設定
    save_name = sava_option + plot_symbol + f"{lat_symbol}{target_latitude:07}{lon_symbol}{target_longitude:08}_azim{sun_azimuth:08}alt{sun_altdeg:07}.html"
    save_filename = os.path.join(save_directory, save_name)
    
    # 3Dプロットの保存
    fig.write_html(save_filename)
    # プロット表示
    webbrowser.open('file:///' + save_filename, new=2)