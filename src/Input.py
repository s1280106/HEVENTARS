# Input.py

"""
ユーザーが使用する入力機能のモジュールです.
The module of input functions used by the user.
"""

# 変数を入力する
# 緯度、経度、太陽（光源）の方位
def validate_input_below(prompt, min_value, max_value):
    """
    Args:
    prompt: 入力された値
    min_value: 値の下限
    max_value: 値の上限
    
    Return:
    value: 緯度、経度、太陽（光源）の方位
    """
    while True:
        try:
            # 値が有効か判別（未満）、小数点以下５桁まで有効
            value = float(input(prompt))
            if min_value <= value < max_value:
                return value
            else:
                print(f"Error: 入力は{min_value}以上{max_value}未満でなければなりません。")
        except ValueError:
            print("Error: 有効な数値を入力してください。")

# 変数を入力する
# 太陽（光源）の仰角
def validate_input_less(prompt, min_value, max_value):
    """
    Args:
    prompt: 入力された値
    min_value: 値の下限
    max_value: 値の上限
    
    Return:
    value: 太陽（光源）の仰角
    """
    while True:
        try:
            # 値が有効か判別（以下）、小数点以下５桁まで有効
            value = float(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Error: 入力は{min_value}以上{max_value}以下でなければなりません。")
        except ValueError:
            print("Error: 有効な数値を入力してください。")

# 機能の有効化を判別する
# y / n
def validate_input_yes_no(prompt):
    """
    Args:
    prompt: 入力された値
    
    Return:
    bool: True or False
    """
    while True:
        # 入力を小文字に変換
        user_input = input(prompt).strip().lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print("Error: y 又は n で入力してください。")
            
# 描画範囲を設定する
# プロット管理番号
def validate_input_plot_range(prompt):
    """
    Args:
    prompt: 入力された値
    
    Returns:
    plot_range: プロット管理番号
    viewpoint: 視点の高さ
    """
    while True:
        number = input(prompt).strip()
        # 6,000m range
        if number == '0':
            return 0, 36
        # 3,000m range
        elif number == '1':
            return 1, 20
        # 600m range
        elif number == '2':
            return 2, 3.6
        # 300m range
        elif number == '3':
            return 3, 1.8
        else:
            print("Error: 有効な設定は [0, 1, 2, 3] のいずれかです。")
