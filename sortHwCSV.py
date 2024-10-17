import zipfile
import csv
import time
from datetime import datetime

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

# Parsing utility functions
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
                    header = next(csv_reader, None)

                    path_parts = file_name.split('/')
                    market = path_parts[1]
                    ticker = path_parts[3].replace('.csv', '')

                    for row in csv_reader:
                        if len(row) < 7:
                            continue

                        date_str, low, open_price, volume, high, close, adj_close = row[:7]
                        date = parse_date(date_str)
                        if not date:
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

                        if date not in stock_data_by_date:
                            stock_data_by_date[date] = {}
                        key = f"{market}-{ticker}"
                        stock_data_by_date[date][key] = stock_data

    return stock_data_by_date

# Sorting algorithms

def partition(arr, low, high):
    pivot = arr[high]  # Choose the last element as pivot
    i = low - 1        # Index of smaller element
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # Swap

    arr[i + 1], arr[high] = arr[high], arr[i + 1]  # Swap pivot element to the correct position
    return i + 1

def iterative_quicksort(arr):
    stack = [(0, len(arr) - 1)]

    while stack:
        low, high = stack.pop()

        if low < high:
            pi = partition(arr, low, high)
            stack.append((low, pi - 1))
            stack.append((pi + 1, high))

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

# CSV writing functions

def write_avg_data_to_csv(stock_data_map, output_file):
    avg_data = {}

    for date, tickers in stock_data_map.items():
        for ticker_key, stock_data in tickers.items():
            ticker = ticker_key.split('-')[1]
            market = stock_data.market
            if ticker not in avg_data:
                avg_data[ticker] = {
                    'market': market,
                    'lowest': stock_data.low,
                    'highest': stock_data.high,
                    'total_volume': stock_data.volume,
                    'count': 1,
                    'start_date': date,
                    'end_date': date
                }
            else:
                avg_data[ticker]['lowest'] = min(avg_data[ticker]['lowest'], stock_data.low)
                avg_data[ticker]['highest'] = max(avg_data[ticker]['highest'], stock_data.high)
                avg_data[ticker]['total_volume'] += stock_data.volume
                avg_data[ticker]['count'] += 1
                avg_data[ticker]['start_date'] = min(avg_data[ticker]['start_date'], date)
                avg_data[ticker]['end_date'] = max(avg_data[ticker]['end_date'], date)

    sorted_avg_data = sorted(avg_data.items())  # Sort by ticker

    with open(output_file, mode='w', newline='') as csvfile:
        fieldnames = ['Ticker', 'Market', 'Lowest Value', 'Highest Value', 'Average Volume', 'Period']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        
        for ticker, data in sorted_avg_data:  # Use sorted data here
            avg_volume = data['total_volume'] / data['count'] if data['count'] > 0 else 0
            period = f"{data['start_date']} - {data['end_date']}"
            writer.writerow([ticker, data['market'], data['lowest'], data['highest'], avg_volume, period])

def write_sorted_data_to_csv(stock_data_map, output_file):
    dates = list(stock_data_map.keys())

    # Sort dates using any sorting algorithm you prefer
    merge_sort(dates)
    insertion_sort(dates)
    iterative_quicksort(dates)

    with open(output_file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Tickers & Market'])

        for date in dates:
            tickers = stock_data_map[date]
            market_ticker_pairs = [f"({data.ticker}, {data.market})" for key, data in tickers.items()]
            writer.writerow([f"{date}: {', '.join(market_ticker_pairs)}"])


# Main Execution
if __name__ == "__main__":
    start_time = time.time()

    zip_file_path = "C:\\cygwin64\\home\\tommy\\322hw\\archive.zip"
    stock_data_by_date = read_zip_data(zip_file_path)

    sorted_output_file = "C:\\cygwin64\\home\\tommy\\322hw\\sorted_stock_data.csv"
    write_sorted_data_to_csv(stock_data_by_date, sorted_output_file) 

    averages_output_file = "C:\\cygwin64\\home\\tommy\\322hw\\averages.csv"
    write_avg_data_to_csv(stock_data_by_date, averages_output_file)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time} seconds")
    print("CSV files generated successfully.")
