from fastapi import FastAPI
from dotenv import load_dotenv
import os
import requests
import csv
from fastapi.responses import FileResponse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

load_dotenv()
API_INTRADAY_KEY = os.getenv("ALPHA_VANTAGE_API_INTRADAY_KEY")
API_RAW_KEY = os.getenv("ALPHA_VANTAGE_API_RAW_KEY")
BASE_URL = "https://www.alphavantage.co/query"

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from the backend!"}

# Default parameters for the API call
params_intraday = {
    "function": "TIME_SERIES_INTRADAY",
    "interval": "60min",  
    "apikey": API_INTRADAY_KEY,
    "datatype": "csv",   
    "outputsize": "full" 
}

params_raw = {
    "function": "TIME_SERIES_DAILY",
    "apikey": API_RAW_KEY,
    "datatype": "csv",
    "outputsize": "full"
}

@app.get("/stock/full-history/{symbol}")
def get_full_history(symbol: str, start_date: str, end_date: str): 
    """
    Fetches stock data from start_date to end_date and writes it to a single CSV file.
    """
    start = datetime.strptime(start_date, "%Y-%m")
    end = datetime.strptime(end_date, "%Y-%m")
    current = start

    file_name = f"{symbol}_full_history.csv"
    with open(file_name, "w", newline="") as csvfile:
        writer = None 

        while current <= end:
            month = current.strftime("%Y-%m")
            params_intraday["symbol"] = symbol
            params_intraday["month"] = month

            response = requests.get(BASE_URL, params=params_intraday)
            if response.status_code == 200:
                csv_data = response.text
                rows = csv_data.splitlines()

                if writer is None:
                    writer = csv.writer(csvfile)
                    writer.writerow(rows[0].split(",")) 

                for row in rows[1:]:
                    writer.writerow(row.split(","))
            else:
                print(f"Error fetching data for {month}: {response.status_code}")

            current += timedelta(days=30)

    return FileResponse(file_name, media_type="text/csv", filename=file_name)

def plot_stock_data(file_name):
    dates = []
    close_prices = []

    with open(file_name, "r") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader) 
        for row in reader:
            if len(row) > 4:
                dates.append(row[0]) 
                close_prices.append(float(row[4]))  

    plt.figure(figsize=(10, 5))
    plt.plot(dates, close_prices, label="Close Price")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.title("Stock Data Over Time")
    plt.xticks(dates[::max(1, len(dates)//10)], rotation=45) 
    plt.legend()
    plt.tight_layout()
    plt.show()

#investment by dollar amount
def plot_invested_stock_data(file_name, investment):
    dates = []
    close_prices = []
    invested_prices = []

    with open(file_name, "r") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader) 
        for row in reader:
            if len(row) > 4:
                dates.append(row[0]) 
                close_prices.append(float(row[4]))  
                invested_prices.append(float(row[4]) * investment)

    plt.figure(figsize=(10, 5))
    plt.plot(dates, invested_prices, label="Invested Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Stock Data Over Time")
    plt.xticks(dates[::max(1, len(dates)//10)], rotation=45) 
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_shares_performance(file_name, numShares):
    dates = []
    close_prices = []
    invested_prices = []

    with open(file_name, "r") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader) 
        for row in reader:
            if len(row) > 4:
                dates.append(row[0]) 
                close_prices.append(float(row[4]))  
                invested_prices.append(float(row[4]) * numShares)

    plt.figure(figsize=(10, 5))
    plt.plot(dates, invested_prices, label="Invested Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Stock Data Over Time")
    plt.xticks(dates[::max(1, len(dates)//10)], rotation=45) 
    plt.legend()
    plt.tight_layout()
    plt.show()


    
#sample query for raw data

#https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=demo
    
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
    
def plot_raw_stock_data(file_name):
    dates = []
    close_prices = []

    with open(file_name, "r") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader) 
        for row in reader:
            if len(row) > 4:
                dates.append(row[0]) 
                close_prices.append(float(row[4]))  

    plt.figure(figsize=(10, 5))
    plt.plot(dates, close_prices, label="Close Price")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.title("Stock Data Over Time")
    plt.xticks(dates[::max(1, len(dates)//10)], rotation=45) 
    plt.legend()
    plt.tight_layout()
    plt.show()