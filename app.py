from flask import Flask, Markup, render_template
import json

import pandas_datareader as dr
import datetime as dt
import datedelta as dd


app = Flask(__name__)

#set data from current to previous month
end = dt.datetime.today()
start = end - dd.MONTH

#Download Stocks From yahoo
stocks = ['CORN', 'UGA', 'NDAQ']
data = dr.data.get_data_yahoo(stocks,start,end)

#Select only closing price and reset index
data = data.Close
data = data.reset_index()
data.Date = data.Date.astype(str)

#Build datatable for javascript
dataTable = [data.columns.tolist()] + data.values.tolist()

#Moving average total using rolling method and take the last record as a prediction
mav = data.tail(3).rolling(window=3).mean().round(2)
pred = mav.tail(1).to_html(index=False,classes='tbl').replace('Symbols', 'Stock')



@app.route('/')
def line():
    return render_template('line_chart.html', data=json.dumps(dataTable), pred=pred)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')