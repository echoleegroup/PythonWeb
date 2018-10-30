import os
from crawler import crawler
from connectMySQL import connect
from calculation import stock_info

from flask import Flask, send_file, render_template, request, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app) #bootstrap

@app.route("/")
def main():
    stockid_tuple = connect.query_list("select stock_id from stock_list")
    stock_list = list()
    for stockid in stockid_tuple:
        stock_list.append(str(stockid[0]))

    return render_template('index.html', stock_list=stock_list)

@app.route('/getStock/<string:stockid>/<int:year>/<int:monthStart>/<int:monthEnd>')
def getStock(stockid, year, monthStart, monthEnd):
    return crawler.getStock(stockid, year, monthStart, monthEnd)

@app.route('/getMonthStock/<string:stockid>')
def getMonthStock(stockid):
    return crawler.getMonthStock(stockid)

@app.route('/getTodayStock')
def getTodayStock():
    return crawler.getTodayStock()

@app.route('/getMA', methods = ['POST', 'GET'])
def getMA():
    ma_stock = request.form
    ma = stock_info.getMA(ma_stock['stock_id'], ma_stock['days'])
    return str(ma)

# Everything not declared before (not a Flask route / API endpoint)...

@app.route('/<path:path>')
def route_frontend(path):
    # ...could be a static file needed by the front end that
    # doesn't use the `static` path (like in `<script src="bundle.js">`)
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_file(file_path)
    # ...or should be handled by the SPA's "router" in front end
    else:
        index_path = os.path.join(app.static_folder, 'index.html')
        return send_file(index_path)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
