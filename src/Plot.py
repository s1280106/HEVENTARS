# Plot.py

"""
標高データ、陰影起伏、緯度経度情報をもとに3Dプロットを返すモジュールです。
This module returns 3D plots based on elevation data, hillshade, and latitude/longitude information.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 3Dプロットを作成
def plot_3d(selected_data, haversine_data, surface, selected_x, selected_y,
            target_latitude, target_longitude, sun_azimuth, sun_altdeg,
            plot_range, viewpoint, smoothing_active, ortho_active):
    """
    Args:
    selected_data: 指定範囲の標高データ
    haversine_data: 曲率補正された標高データ
    surface: 表現方式（陰影起伏 or オルソ画像）
    selected_x: 指定範囲の経度データ
    selected_y: 指定範囲の緯度データ
    target_latitude: ターゲットの緯度
    target_longitude: ターゲットの経度
    sun_azimuth: 太陽（光源）の方位
    sun_altdeg: 太陽（光源）の仰角
    plot_range: プロット管理番号
    viewpoint: 視点の高さ
    smoothing_active: スムージングの有効化
    ortho_active: オルソ画像の使用
    
    Return:
    fig: 3Dプロット
    """
    
    print("3Dプロットの構築中...")
    
    fig = go.Figure()
    
    # 通常のホバー表示設定
    normal_hover = "Lat : %{y}<br>Lon: %{x}<br>Apparent elevation: %{z}<extra></extra>"
    # 標高データのプロット
    surface_plot = go.Surface(
        z=haversine_data, x=selected_x, y=selected_y,
        colorscale='gray',
        showscale=False,
        surfacecolor=surface,
        opacity=1,
        hoverinfo="x+y+z",
        hovertemplate=normal_hover,
        lightposition=dict(x=1, y=1, z=1)
    )
    
    # ターゲット地点付近の標高を取得 標高データの中央
    center_x = int(selected_data.shape[1] / 2)
    center_y = int(selected_data.shape[0] / 2)
    target_elevation = selected_data[center_y, center_x]
    # ターゲットマーカーの高度設定（視点の邪魔にならないように）
    target_marker_elevation = target_elevation + 0.2
    
    # ターゲットマーカーのホバー表示設定
    target_hover=f'Lat: {target_latitude}<br>Lon: {target_longitude}<br>Hight: {target_elevation}'
    # Target地点にマーカーを追加
    target_marker = go.Scatter3d(
        x=[target_longitude],
        y=[target_latitude],
        z=[target_marker_elevation],
        mode='markers',
        marker=dict(size=3, color='#EE82EE', symbol='circle', opacity=1),
        hovertemplate=target_hover,
        hoverinfo='text+name',
        name="Rover is here!",
    )
    
    # plot_rangeによる変数設定
    # z軸の範囲、x,y軸の間隔、抽出範囲を示すテキスト
    if plot_range == 0:   # range: 6,000m
        z_range = 3000
        axis_span = 0.02
        range_txt = "6,000m"
    elif plot_range == 1: # range: 3,000m
        z_range = 1500
        axis_span = 0.01
        range_txt = "3,000m"
    elif plot_range == 2: # range: 600m
        z_range = 300 
        axis_span = 0.003
        range_txt = "600m"
    else:                 # range: 300m
        z_range = 150 
        axis_span = 0.001
        range_txt = "300m"
    
    # 方角マーカーの高さを設定
    direction_elevation = np.median(selected_data) + (z_range/2)
    # 方角を示すマーカーを追加（東）
    east_marker = go.Scatter3d(
        x=[np.max(selected_x)],
        y=[target_latitude],
        z=[direction_elevation],
        mode='markers',
        marker=dict(size=4, color="#0000FF", symbol='diamond', opacity=1),
        hoverinfo='name',
        name="East",
    )
    # 方角を示すマーカーを追加（西）
    west_marker = go.Scatter3d(
        x=[np.min(selected_x)],
        y=[target_latitude],
        z=[direction_elevation],
        mode='markers',
        marker=dict(size=4, color="#DAA520", symbol='diamond', opacity=1),
        hoverinfo='name',
        name="West",
    )
    # 方角を示すマーカーを追加（南）
    south_marker = go.Scatter3d(
        x=[target_longitude],
        y=[np.min(selected_y)],
        z=[direction_elevation],
        mode='markers',
        marker=dict(size=4, color="#FF0000", symbol='diamond', opacity=1),
        hoverinfo='name',
        name="South",
    )
    # 方角を示すマーカーを追加（北）
    north_marker = go.Scatter3d(
        x=[target_longitude],
        y=[np.max(selected_y)],
        z=[direction_elevation],
        mode='markers',
        marker=dict(size=4, color="#8A2BE2", symbol='diamond', opacity=1),
        hoverinfo='name',
        name="North",
    )
    
    # z軸描画範囲の設定
    # 中央値を基準とする
    standard_elevation = np.median(selected_data)
    z_min = standard_elevation - z_range
    z_max = standard_elevation + z_range
    
    # タイトルテキスト
    parameter_txt0 = f'"HEVENTARS" simulation at ({target_latitude}, {target_longitude}) in plot range {range_txt} per side.'
    parameter_txt1 = f'"HEVENTARS" simulation at ({target_latitude}, {target_longitude}) in plot range {range_txt} per side. Smoothing is on.'
    parameter_txt2 = f'<br>Expression method is hill shade; sun azimuth is {sun_azimuth} and sun altdeg is {sun_altdeg}.'
    parameter_txt3 = f'<br>Expression method is ortho image from KAGUYA.'
    # タイトルの設定
    if smoothing_active == False:
        if ortho_active == False:
            # スムージングなし、陰影起伏
            title_txt = parameter_txt0 + parameter_txt2
        else:
            # スムージングなし、オルソ画像
            title_txt = parameter_txt0 + parameter_txt3
    else:
        if ortho_active == False:
            # スムージングあり、陰影起伏
            title_txt = parameter_txt1 + parameter_txt2
        else:
            # スムージングあり、オルソ画像
            title_txt = parameter_txt1 + parameter_txt3
    
    # 軸の設定
    layout = go.Layout(
        scene=dict(
            xaxis=dict(
                title='Longitude',
                backgroundcolor="rgb(0, 0, 40, 0.5)",
                gridcolor="#C0C0C0",
                gridwidth=4,
                dtick=axis_span,),
            yaxis=dict(
                title='Latitude',
                backgroundcolor="rgb(0, 0, 40, 0.5)",
                gridcolor="#C0C0C0",
                gridwidth=4,
                dtick=axis_span,),
            zaxis=dict(
                title='Elevation',
                backgroundcolor="rgb(0, 0, 40, 0.5)",
                gridcolor="#918D40",
                gridwidth=3,
                range=[z_min, z_max]),
            # 通常のアスペクト比（変更の必要なければこのまま）
            aspectmode="manual",
            aspectratio=dict(x=1, y=1, z=1)
            
            # アスペクト比の設定はコチラ
            # Area.py 及び Ortho.py の抽出範囲の変更をあわせて推奨します。
            #aspectratio=dict(x=1, y=5, z=1)
        ),
        margin=dict(l=0, r=0, b=0, t=60),
        title=title_txt,
    )
    
    # カメラの center, eye のZベクトルを探査機目線になるように求める
    z_distance = (target_elevation + viewpoint - standard_elevation + z_range)/(z_range*2) - 0.5
    # カメラの設定
    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=z_distance),
        eye=dict(x=0, y=0, z=z_distance)
        )
    
    # サブプロットを作成
    fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'surface'}]])

    # surfaceを追加
    fig.add_trace(surface_plot, row=1, col=1)
    # ターゲットマーカーを追加
    fig.add_trace(target_marker, row=1, col=1)
    # 方角マーカーを追加
    fig.add_trace(east_marker, row=1, col=1)
    fig.add_trace(west_marker, row=1, col=1)
    fig.add_trace(south_marker, row=1, col=1)
    fig.add_trace(north_marker, row=1, col=1)

    # レイアウトを更新
    fig.update_layout(layout, scene_camera=camera, showlegend=False)
    
    # プロットを返す
    return fig