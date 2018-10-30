import os
from crawler import crawler
from connectMySQL import connect

from flask import Flask, send_file, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app) #bootstrap

@app.route("/")
def main():
    stock_list = connect.query_list("select stock_id from stock_list")
    #index_path = os.path.join(app.static_folder, '../templates/bootstrap/basic.html')
    index_path = os.path.join(app.static_folder, '../templates/index.html')
    return send_file(index_path)

@app.route('/getStock/<string:stockid>/<int:year>/<int:monthStart>/<int:monthEnd>')
def getStock(stockid, year, monthStart, monthEnd):
    return crawler.getStock(stockid, year, monthStart, monthEnd)

@app.route('/getMonthStock/<string:stockid>')
def getMonthStock(stockid):
    return crawler.getMonthStock(stockid)

@app.route('/getTodayStock')
def getTodayStock():
    return crawler.getTodayStock()

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
