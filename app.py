from flask import Flask, render_template, request, jsonify
from Mybybit import mybybit  
from Myokx import myokx

app = Flask(__name__,template_folder='template')

import os

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        function = request.form['function']
        api_key = request.form['apiKey']
        secret_key = request.form['secretKey']
        password = request.form['password']
        
        # 初始化你的Bybit API类并传入提供的凭据
        bybit = mybybit(api_key, secret_key, password)
        
        # 根据用户选择的功能调用相应的方法
        result = None
        if function == 'balance':
            result = bybit.balance('BTC')
        elif function == 'position':
            result = bybit.position('BTCUSD')
        elif function == 'setLever':
            result = bybit.setLever('BTCUSD', 10)
        elif function == 'fundingRatio':
            result = bybit.fundingRatio('BTCUSD')
        elif function == 'price':
            result = bybit.price('BTCUSD')
        elif function == 'bybitTime':
            result = bybit.bybitTime()
        elif function == 'trade':
            result = bybit.trade('BTCUSD', 'Buy', 'Limit', '66000', '0.1')
        
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

