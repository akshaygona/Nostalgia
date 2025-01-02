from fastapi import FastAPI
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
import requests
import csv

load_dotenv()
#API_INTRADAY_KEY = os.getenv("ALPHA_VANTAGE_API_INTRADAY_KEY") #useless in the end too many api calls needed and i am broke
API_DAILY_KEY = os.getenv("ALPHA_VANTAGE_API_DAILY_ADJ_KEY")
API_RAW_KEY = os.getenv("ALPHA_VANTAGE_API_RAW_KEY")
BASE_URL = "https://www.alphavantage.co/query"

app = FastAPI()

# Default parameters for the API Daily ADJ key call
params_daily_adjusted = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "interval": "60min",  
    "apikey": API_DAILY_KEY,
    "datatype": "csv",   
    "outputsize": "full" 
}

# Default parameters for the API Raw call
params_raw = {
    "function": "TIME_SERIES_DAILY",
    "apikey": API_RAW_KEY,
    "datatype": "csv",
    "outputsize": "full"
}

def get_adjusted_daily(symbol): #apparently this is a premuim feature god damn it
    params_daily_adjusted["symbol"] = symbol
    response = requests.get(BASE_URL, params=params_daily_adjusted)
    if response.status_code == 200:
        filename = f"{symbol}_adjusted_data.csv"
        with open(filename, "w") as csvfile:
            csvfile.write(response.text)
        return filename
    else:
        print(f"Error fetching data for {symbol}: {response.status_code}")
        return None
    

def plot_adjusted_daily(file_name, start_date="2000-01-01", end_date="2024-12-31"): #apparently this is a premuim feature
    dates = []
    close_prices = []

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    with open(file_name, "r") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader) 
        for row in reader:
            if len(row) > 4:
                date = datetime.strptime(row[0], "%Y-%m-%d")
                close_price = float(row[4])

                if start_date <= date <= end_date:
                    dates.append(date)
                    close_prices.append(close_price)

    dates.reverse()
    close_prices.reverse()

    plt.figure(figsize=(10, 5))
    plt.plot(dates, close_prices, label="Close Price")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.title("Stock Data Over Time")
    plt.xticks(dates[::max(1, len(dates)//10)], rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def get_raw_stock_data(symbol):
    params_raw["symbol"] = symbol
    response = requests.get(BASE_URL, params=params_raw)
    if response.status_code == 200:
        filename = f"{symbol}_raw_data.csv"
        with open(filename, "w") as csvfile:
            csvfile.write(response.text)
        return filename
    else:
        print(f"Error fetching data for {symbol}: {response.status_code}")
        return None

def plot_raw_stock_data(file_name, start_date="2000-01-01", end_date="2024-12-31"):
    dates = []
    close_prices = []

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    with open(file_name, "r") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader) 
        for row in reader:
            if len(row) > 4:
                date = datetime.strptime(row[0], "%Y-%m-%d")
                close_price = float(row[4])

                if start_date <= date <= end_date:
                    dates.append(date)
                    close_prices.append(close_price)

    dates.reverse()
    close_prices.reverse()

    plt.figure(figsize=(10, 5))
    plt.plot(dates, close_prices, label="Close Price")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.title("Stock Data Over Time")
    plt.xticks(dates[::max(1, len(dates)//10)], rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


#get_raw_stock_data("AAPL")
#get_adjusted_daily("AAPL") #premium key required smh

plot_raw_stock_data("AAPL_raw_data.csv")
#plot_adjusted_daily("AAPL_adjusted_data.csv") #premium key required smh