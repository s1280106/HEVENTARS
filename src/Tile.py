# Tile.py

"""
入力された座標情報をもとにその地点が含まれるタイルの名前を返すモジュールです。
This module returns the name of the tile containing the point based on the input coordinate information.
"""

# 定数
DEGREE_INTERVAL = 3
MAX_LONGITUDE = 360

"""
与えられた緯度経度に含まれるタイルを見つけ、タイル名を生成する関数。
タイル名は北半球では緯度の前半分が大きくなるように生成される、南半球はその逆。
緯度が0~-3の範囲は特殊なタイル名になる。
"""

# タイル名を生成する
def generate_name(latitude, longitude):
    """
    Args:
    latitude: ターゲットの緯度
    longitude: ターゲットの経度
    
    Returns:
    prefix: 経度の分類
    tile_name: タイルの名前
    """
    
    print("タイル名の生成中...")
    
    # 緯度がマイナスの場合、南半球の処理
    if latitude < 0:
        if 0 > latitude > -3:
            return generate_name_ex(latitude, longitude)
        else:
            return generate_name_south(latitude, longitude)
    else:
        return generate_name_north(latitude, longitude)
    
    
# 南半球かつ緯度が0から-3の場合のタイル名を生成する関数
def generate_name_ex(latitude, longitude):
    # 緯度と経度を3度ごとに丸める
    latitude = int(latitude / DEGREE_INTERVAL) * DEGREE_INTERVAL
    longitude = int((longitude + MAX_LONGITUDE) % MAX_LONGITUDE / DEGREE_INTERVAL) * DEGREE_INTERVAL
    
    # 緯度を正にしてプレフィックスを変更
    latitude = abs(latitude)
    lat_prefix1 = 'N'
    lat_prefix2 = 'S'
    prefix = f'lon{abs(longitude):03}'
    tile_name = f'{lat_prefix1}00E{abs(longitude):03}{lat_prefix2}{abs(latitude + DEGREE_INTERVAL):02}E{abs(longitude + DEGREE_INTERVAL):03}'
    return prefix, tile_name


# 北半球の場合のタイル名を生成する関数
def generate_name_north(latitude, longitude):
    # 緯度と経度を3度ごとに丸める
    latitude = int(latitude / DEGREE_INTERVAL) * DEGREE_INTERVAL
    longitude = int((longitude + MAX_LONGITUDE) % MAX_LONGITUDE / DEGREE_INTERVAL) * DEGREE_INTERVAL
    
    lat_prefix = 'N'
    prefix = f'lon{abs(longitude):03}'
    tile_name = f'{lat_prefix}{abs(latitude + DEGREE_INTERVAL):02}E{abs(longitude):03}{lat_prefix}{abs(latitude):02}E{abs(longitude + DEGREE_INTERVAL):03}'
    return prefix, tile_name

# 南半球の場合のタイル名を生成する関数
def generate_name_south(latitude, longitude):
    # 緯度と経度を3度ごとに丸める
    latitude = int(latitude / DEGREE_INTERVAL) * DEGREE_INTERVAL
    longitude = int((longitude + MAX_LONGITUDE) % MAX_LONGITUDE / DEGREE_INTERVAL) * DEGREE_INTERVAL
    
    # 緯度を正にしてプレフィックスを変更
    latitude = abs(latitude)
    lat_prefix = 'S'
    prefix = f'lon{abs(longitude):03}'
    tile_name = f'{lat_prefix}{abs(latitude):02}E{abs(longitude):03}{lat_prefix}{abs(latitude + DEGREE_INTERVAL):02}E{abs(longitude + DEGREE_INTERVAL):03}'
    return prefix, tile_name
