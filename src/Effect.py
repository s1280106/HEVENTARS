# Effect.py

"""
与えられたデータに計算処理を行うモジュールです。
This module performs computational processing on the given data.
"""

from matplotlib.colors import LightSource
from scipy.ndimage import gaussian_filter

# hillshadeを計算
def calculate_hillshade(elevation_data, azdeg, altdeg):
    """
    Args:
    elevation_data: 標高データ
    azdeg: 太陽（光源）の方位
    altdeg: 太陽（光源）の仰角
    
    Return: 
    hillshade: 陰影起伏
    """
    
    print("陰影起伏の計算中...")
    
    ls = LightSource(azdeg, altdeg)
    hillshade = ls.hillshade(elevation_data, vert_exag=1.0, dx=1, dy=1, fraction=1)
    return hillshade

# データのスムージング
def smoothing_data(data):
    """
    Arg:
    data: 多次元配列データ
    
    Return: 
    smoothed_data: スムージング処理後のデータ
    """
    
    print("スムージング処理の実行中...")
    
    smoothed_data = gaussian_filter(data, sigma=3)
    return smoothed_data