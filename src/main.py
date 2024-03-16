# main.py

"""
月の標高データを用いて、探査機目線で月地形の可視化を行うソフトウェア "HEVENTARS" （ヘーヴェンタース）のメインファイルです。
This is the main file of the software "HEVENTARS", which visualizes the topography of the Moon from the rover's viewpoint using lunar elevation data.
"""

import Input as input
import Tile as tile
import Download as dl
import Read_lbl as read
import Area as area
import Effect as ef
import Plot as pl
import Save as sv
import Ortho as ort

if __name__ == "__main__":
    
    # 調査地点の入力
    print("=== 調査対象とする地点を指定 ===")
    # 緯度経度の入力
    target_latitude = input.validate_input_below("・緯度を入力してください。\n北緯を正、南緯を負とする(-90以上90未満): ", -90, 90)
    target_longitude = input.validate_input_below("・経度を入力してください。\n（東周り0以上360未満の間）: ", 0, 360)
    # 月からの太陽の方位と高度の入力
    sun_azimuth = input.validate_input_below("・太陽の方位を入力してください。\n北0度、東90度、南180度、西270度（0以上360未満の間）: ", 0, 360)
    sun_altdeg = input.validate_input_less("・太陽の仰角（高度）を入力してください。\n地平線0度、直上90度（0から90度の間）: ", 0, 90)
    # スムージング機能の有効化
    smoothing_active = input.validate_input_yes_no("・データにスムージングを適応しますか？\n（より滑らかな描画を可能にするが、実際のデータからは変化します） <y/n> : ")
    # 描画範囲の設定
    plot_range, viewpoint = input.validate_input_plot_range("・プロットの描画範囲を [0, 1, 2, 3] のいずれかで設定してください。\n[0: 6,000m, 1: 3,000m, 2: 600m, 3: 300m] : ")
    # オルソ画像の貼り付け
    ortho_active = input.validate_input_yes_no("・オルソ画像を貼り付けますか？\n（陰影起伏は無効化されます） <y/n> : ")
    
    
    # 対象地点を含むタイルを調べる
    prefix, tile_name = tile.generate_name(target_latitude, target_longitude)
    
    # 該当するタイルをダウンロード
    img_path, lbl_path = dl.download_data(prefix, tile_name)
    
    # lblファイルから情報を取得する
    lbl_keys = ["BANDS", "LINES", "LINE_SAMPLES", "UPPER_LEFT_LATITUDE",
                        "UPPER_LEFT_LONGITUDE", "MAP_RESOLUTION"]
    topographic_info = read.get_lbl(lbl_path, lbl_keys)
    
    # 標高データを取得する
    LINE_SAMPLES = int(topographic_info.get("LINE_SAMPLES"))
    LINES = int(topographic_info.get("LINES"))
    elevation_data = area.get_elevation(img_path, LINE_SAMPLES, LINES)
    
    # 描画範囲のデータを抽出する
    UPPER_LEFT_LATITUDE = topographic_info.get("UPPER_LEFT_LATITUDE")
    UPPER_LEFT_LONGITUDE = topographic_info.get("UPPER_LEFT_LONGITUDE")
    MAP_RESOLUTION = topographic_info.get("MAP_RESOLUTION")
    selected_data, selected_x, selected_y, haversine_data = area.select_area(elevation_data, target_latitude, target_longitude, 
                                                            LINE_SAMPLES, LINES, UPPER_LEFT_LATITUDE,
                                                            UPPER_LEFT_LONGITUDE, MAP_RESOLUTION, plot_range)

    # オルソ画像を使用する場合
    if ortho_active == True:
        # オルソ画像を取得し、抽出する
        ortho_img_path, ortho_lbl_path = dl.download_ortho(prefix, tile_name)
        ortho_image = ort.get_ortho(ortho_img_path, LINES, LINE_SAMPLES)
        selected_ortho = ort.selected_ortho(ortho_image, target_latitude, target_longitude, 
                                            LINE_SAMPLES, LINES,UPPER_LEFT_LATITUDE, UPPER_LEFT_LONGITUDE, 
                                            MAP_RESOLUTION, plot_range)
    # オルソ画像を使用しない場合
    else:
        # 陰影起伏を計算する
        hillshade = ef.calculate_hillshade(haversine_data, sun_azimuth, sun_altdeg)
    
    # スムージングが有効の場合
    if smoothing_active == True:
        # 標高データに対してスムージング
        adjusted_data = ef.smoothing_data(haversine_data)
        if ortho_active == False:
            # かつ陰影起伏を使用する場合、スムージング
            adjusted_surface = ef.smoothing_data(hillshade)
        else:
            # かつオルソ画像を使用する
            adjusted_surface = selected_ortho
    # スムージングが無効の場合
    else:
        # 標高データはそのまま
        adjusted_data = selected_data
        if ortho_active == False:
        # かつ陰影起伏を使用する
            adjusted_surface = hillshade
        else:
        # かつオルソ画像を使用する
            adjusted_surface = selected_ortho

    # 3Dプロットを作成する
    fig = pl.plot_3d(adjusted_data, haversine_data, adjusted_surface, selected_x, selected_y,
                target_latitude, target_longitude, sun_azimuth, sun_altdeg,
                plot_range, viewpoint, smoothing_active, ortho_active)

    # 3Dプロットを保存して展開する
    sv.save_expand(fig, target_latitude, target_longitude, sun_azimuth, sun_altdeg, 
                smoothing_active, ortho_active, plot_range)