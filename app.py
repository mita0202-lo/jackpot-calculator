# 檔案：app.py (v4)

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    # 新增 main_pool_current 的預設值
    defaults = {
        "sub_pool_cap": 100000.0,
        "main_pool_base": 100000.0,
        "total_contribution_rate": 0.5,
        "main_pool_share_percentage": 30.0,
        "sub_pool_current": 0.0,
        "main_pool_current": 0.0,  # 【新】增加主池當前餘額
        "main_bet": 0.0,
    }

    results = {}
    current_values = defaults.copy()

    if request.method == 'POST':
        form_values = {}
        for key in defaults:
            form_value = request.form.get(key)
            if form_value and form_value.strip():
                try:
                    form_values[key] = float(form_value)
                except ValueError:
                    form_values[key] = defaults[key]
            else:
                form_values[key] = defaults[key]

        current_values = form_values
        action = request.form.get('action')

        if action == '計算注資':
            # 讀取所有需要的當前值
            sub_pool_current = form_values['sub_pool_current']
            main_pool_current = form_values['main_pool_current']  # 【新】讀取主池餘額
            main_bet = form_values['main_bet']
            sub_pool_cap = form_values['sub_pool_cap']

            total_rate_decimal = form_values['total_contribution_rate'] / 100.0
            main_share_decimal = form_values['main_pool_share_percentage'] / 100.0
            sub_share_decimal = 1.0 - main_share_decimal

            total_contribution_amount = main_bet * total_rate_decimal
            potential_sub_contribution = total_contribution_amount * sub_share_decimal

            space_in_sub_pool = sub_pool_cap - sub_pool_current
            if space_in_sub_pool < 0:
                space_in_sub_pool = 0

            actual_sub_contribution = min(potential_sub_contribution, space_in_sub_pool)
            actual_main_contribution = total_contribution_amount - actual_sub_contribution

            # 【新】計算兩個獎池的新餘額
            new_sub_pool = sub_pool_current + actual_sub_contribution
            new_main_pool = main_pool_current + actual_main_contribution

            results = {
                'message': '注資計算完成！',
                'contribution_to_sub': f"{actual_sub_contribution:,.2f}",
                'contribution_to_main': f"{actual_main_contribution:,.2f}",
                'new_sub_pool': f"{new_sub_pool:,.2f}",
                'new_main_pool': f"{new_main_pool:,.2f}",  # 【新】將主池新餘額加入結果
            }

        elif action == '模擬Jackpot開獎':
            sub_pool_current = form_values['sub_pool_current']
            main_pool_base = form_values['main_pool_base']

            new_sub_pool_after_win = sub_pool_current - main_pool_base

            results = {
                'message': 'Jackpot 開獎模擬完成！',
                'transferred_amount': f"{main_pool_base:,.2f}",
                'new_sub_pool_after_win': f"{new_sub_pool_after_win:,.2f}",
                'new_main_pool_after_win': f"{main_pool_base:,.2f}"
            }

    return render_template('index.html', results=results, values=current_values)


if __name__ == '__main__':
    app.run(debug=True)