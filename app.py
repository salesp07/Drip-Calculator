from flask import Flask, render_template, request
import yfinance as yf
import math


def get_current_price(ticker):
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]

def frequency(dividends):
    date1 = dividends.index[-1].strftime('%Y-%m-%d')
    date2 = dividends.index[-2].strftime('%Y-%m-%d')
    print(date1, date2)

    year1 = date1[0:4]
    year2 = date2[0:4]

    month1 = date1[5:7]
    month2 = date2[5:7]


    if year1 == year2:
        difference = int(month1) - int(month2)
    else:
        difference = int(month1) + (12 - int(month2))

    if difference == 1:
        difference = "Monthly"
    elif difference == 3:
        difference = "Quarterly"
    elif difference == 6:
        difference = "Semi-Annually"
    elif difference == 12:
        difference = "Annually"
    else:
        difference = "Unknown"

    return difference

def calculate(price, latest):
    drip = math.ceil(price / latest)
    return drip



def main(symbol):
    ticker = yf.Ticker(symbol)

    try:
        current_price = get_current_price(ticker)
    except:
        return ["Please enter a valid symbol.", "", "", "", ""]

    dividends = yf.Ticker(symbol).dividends

    if dividends.size == 0:
        return [symbol.upper() + " doesn't pay out dividends.", "", "", "", ""]
    elif dividends.size == 1:
        div_frequency = "Unknown"
    else:
        div_frequency = frequency(dividends)


    latest = dividends[-1]
    drip = calculate(current_price, latest)

    
    s = [symbol.upper()]
    s.append("Current Price: $" + format(current_price, '.2f'))
    s.append("Dividend Frequency: " + div_frequency)
    s.append("Dividend Amount: $" + str(latest))
    s.append("DRIP: " + str(drip) + " shares or $" + format((drip * current_price), '.2f'))

    return s

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        ticker = request.form["symbol"]
        array = main(ticker)
        return render_template("home.html", content1=array[0], content2=array[1], content3=array[2], content4=array[3], content5=array[4])
    else:
        return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)