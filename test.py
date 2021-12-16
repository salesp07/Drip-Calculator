import pandas as pd
import yfinance as yf
import math



def get_current_price(ticker):
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]

def frequency(dividends):
    date1 = dividends.index[-1].strftime('%Y-%m-%d')
    date2 = dividends.index[-2].strftime('%Y-%m-%d')

    year1 = date1[0:4]
    year2 = date2[0:4]

    month1 = date1[5:7]
    month2 = date2[5:7]


    if year1 == year2:
        difference = int(month1) - int(month2)
    else:
        difference = int(month1) + (12 - int(month2))

    if difference == 1:
        difference = "Month"
    elif difference == 3:
        difference = "Quarter"
    elif difference == 6:
        difference = "6 Months"
    elif difference == 12:
        difference = "Year"

    return difference

def calculate(price, latest):
    drip = math.ceil(price / latest)
    return drip

def main(symbol):
    ticker = yf.Ticker(symbol)
    current_price = get_current_price(ticker)

    dividends = yf.Ticker(symbol).dividends
    div_frequency = frequency(dividends)

    latest = dividends[-1]
    drip = calculate(current_price, latest)

    s = "<p>1 APPL share is currently worth $" + format(current_price, '.2f') + "</p>"
    s += "<p>Apple pays dividends every " + div_frequency + "</p>"
    s += "<p>The last dividend was in the value of $" + str(latest) + "</p>"
    s += "<p>To get a DRIP, you will need " + str(drip) + " shares." + "</p>"

    return s

ticker = yf.Ticker("tsla")
print(yf.Ticker("tsla").dividends)



