# SLIM.py

"""
"HEVENTARS" （ヘーヴェンタース）のカスタマイズモジュールです。
小型月着陸実証機 SLIM 専用に設計されています。
標高データとして、KAGUYA ではなく LRO の観測データを使用しています。
SLIM 関係のプロットを行う場合、main.py ではなく SLIM.py を実行してください。

This is "HEVENTARS" customization module.
It is designed specifically for Smart Lander for Investigating Moon (SLIM).
It uses LRO observation data instead of KAGUYA as elevation data.
To plot SLIM-related plots, run LRO.py instead of main.py.
"""

import Area as area
import Effect as ef
import Plot as pl
import Save as sv

"""
LRO 観測データ： https://pds.lroc.asu.edu/data/LRO-L-LROC-5-RDR-V1.0/LROLRC_2001/DATA/SDP/NAC_DTM/THEOPHILUS3/
    標高:   NAC_DTM_THEOPHILUS3.tif
    ラベル: NAC_DTM_THEOPHILUS3.LBL
        
    データ領域： (-12.5816902, 25.0548146) to (-14.0208781, 25.4095815)
    データ型： IEEE浮動小数点数 32bit big endian
"""

# LBLファイルから情報を取得
# データサイズ
LINES, LINE_SAMPLES = 14547, 3494
# 左上の緯度と経度を定義
UPPER_LEFT_LATITUDE = -12.5816902
UPPER_LEFT_LONGITUDE = 25.0548146
# マップスケールを定義 <pixel/deg>
MAP_RESOLUTION = 10107.78347472


if __name__ == "__main__":
    
    print("=== SLIM 専用モジュール実行中 ===")
    
    # ------------ シュミレーション条件の設定 ----------------
    # 標高データのファイル名
    tif_name = "NAC_DTM_THEOPHILUS3.tif"
    # 緯度経度の設定 = [float]
    # データ領域内で設定 (-12.5816902, 25.0548146) to (-14.0208781, 25.4095815)
    target_longitude = 25.2510
    target_latitude = -13.3160
    # 太陽の方位と高度の設定 = [float]
    # azimuth: 北0度、東90度、南180度、西270度（0以上360未満の間）
    # altdeg:  地平線0度、直上90度（0から90度の間） 
    sun_azimuth = 90
    sun_altdeg = 20
    # スムージング機能の有効化 = [bool]
    smoothing_active = False
    # 描画範囲の設定 = [1, 2, 3] 
    # 1: 3,000m, 2: 600m, 3: 300m
    plot_range = 1
    # 月面からの視点の高さ = [float]
    # plot_range に応じたデフォルト設定 <単位: m>
    if plot_range == 1:
        viewpoint = 20
    elif plot_range == 2:
        viewpoint = 3.6
    else:
        viewpoint = 1.8
        
    # オルソ画像の使用（現在、使用不可）= [bool]
    ortho_active = False
    # ------------------------------------------------------
    
    # 標高データを取得する
    elevation_data = area.get_elevation_LRO(tif_name)

    # 描画範囲のデータを抽出する
    selected_data, selected_x, selected_y, haversine_data = area.select_area(elevation_data, target_latitude, target_longitude, 
                                                            LINE_SAMPLES, LINES, UPPER_LEFT_LATITUDE,
                                                            UPPER_LEFT_LONGITUDE, MAP_RESOLUTION, plot_range)
    
    # 陰影起伏の計算
    hillshade = ef.calculate_hillshade(haversine_data, sun_azimuth, sun_altdeg)
    
    # スムージングが有効の場合
    # 地形と陰影起伏に対してスムージングを行う
    if smoothing_active == True:
        adjusted_data = ef.smoothing_data(haversine_data)
        adjusted_hillshade = ef.smoothing_data(hillshade)
    # 無効の場合
    else:
        adjusted_data = selected_data
        adjusted_hillshade = hillshade

    # 3Dプロットの作成
    fig = pl.plot_3d(adjusted_data, haversine_data, adjusted_hillshade, selected_x, selected_y,
                target_latitude, target_longitude, sun_azimuth, sun_altdeg,
                plot_range, viewpoint, smoothing_active, ortho_active)
    
    # 3Dプロットを保存して展開する
    sv.save_expand_LRO(fig, target_latitude, target_longitude, sun_azimuth, sun_altdeg, smoothing_active, plot_range)