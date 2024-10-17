import zipfile
import csv
from datetime import datetime
import time  

class StockData:
    def __init__(self, market, ticker, open_price, high, low, close, volume, adj_close):
        self.market = market
        self.ticker = ticker
        self.open_price = open_price
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.adj_close = adj_close

    def __repr__(self):
        return (f"Market: {self.market}, Ticker: {self.ticker}, Open: {self.open_price}, "
                f"High: {self.high}, Low: {self.low}, Close: {self.close}, "
                f"Volume: {self.volume}, AdjClose: {self.adj_close}")

def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), '%d-%m-%Y').date()
    except ValueError:
        return None

def parse_double(value):
    try:
        return float(value) if value else 0.0
    except ValueError:
        return float('nan')

def read_zip_data(zip_file_path):
    stock_data_by_date = {}

    with zipfile.ZipFile(zip_file_path, 'r') as z:
        for file_name in z.namelist():
            if file_name.endswith(".csv"):
                with z.open(file_name) as f:
                    csv_reader = csv.reader(f.read().decode('utf-8').splitlines())
                    header = next(csv_reader, None)  # Skip header if present
                    
                    # Extract market and ticker from the path
                    path_parts = file_name.split('/')
                    market = path_parts[1]
                    ticker = path_parts[3].replace('.csv', '')

                    for row in csv_reader:
                        if len(row) < 7:
                            print(f"Skipping malformed row: {row}")
                            continue

                        date_str, low, open_price, volume, high, close, adj_close = row[:7]
                        date = parse_date(date_str)
                        if not date:
                            print(f"Error parsing date: {date_str}")
                            continue

                        stock_data = StockData(
                            market,
                            ticker,
                            parse_double(open_price),
                            parse_double(high),
                            parse_double(low),
                            parse_double(close),
                            parse_double(volume),
                            parse_double(adj_close)
                        )

                        # Use date as key in outer map
                        if date not in stock_data_by_date:
                            stock_data_by_date[date] = {}

                        # Use market-ticker as key in the inner map
                        key = f"{market}-{ticker}"
                        stock_data_by_date[date][key] = stock_data

    return stock_data_by_date

# Quicksort with median-of-three pivot selection
def quicksort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)

def partition(arr, low, high):
    mid = (low + high) // 2
    pivot_index = median_of_three(arr, low, mid, high)
    arr[high], arr[pivot_index] = arr[pivot_index], arr[high]
    pivot = arr[high]
    
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def median_of_three(arr, low, mid, high):
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]
    return mid

def sort_by_date(stock_data_map):
    dates = list(stock_data_map.keys())
    
    
    
    quicksort(dates, 0, len(dates) - 1)
    
    
  
    
    return dates

def print_sorted_data(stock_data_map):
    sorted_dates = sort_by_date(stock_data_map)
    #for date in sorted_dates:
     #   print(f"Date: {date}")
        # Uncomment to print detailed stock data
        # for key, stock_data in stock_data_map[date].items():
        #     print(f"  {key}: {stock_data}")

if __name__ == "__main__":
    zip_file_path = "C:\\Users\\tommy\\Downloads\\archive.zip"
    stock_data_by_date = read_zip_data(zip_file_path)
    print("Sorted Stock Data by Date:")
    start_time = time.time() 
    print_sorted_data(stock_data_by_date)
    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time
    print(f"Sorting took {elapsed_time:.6f} seconds.")  # Print elapsed time
    #WHAT DO YOU ALLOCATE HOW IS THIS GOING TO GROW IN TERMS OF STORAGE (Space analysis) 
    #PLOT RESULTS SCATTER PLOT & THEN DRAW LINE THROUGH AVERAGE SIGMA(1-N)/N