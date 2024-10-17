import zipfile
import csv
import random
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

def read_random_records(zip_file_path, n):
    records = []
    files = []

    with zipfile.ZipFile(zip_file_path, 'r') as z:
        files = [file_name for file_name in z.namelist() if file_name.endswith(".csv")]

        # Randomly select n records
        while len(records) < n and files:
            file_name = random.choice(files)
            with z.open(file_name) as f:
                csv_reader = csv.reader(f.read().decode('utf-8').splitlines())
                header = next(csv_reader, None)  # Skip header if present

                for row in csv_reader:
                    if len(row) < 7:
                        continue  # Skip malformed rows

                    date_str, low, open_price, volume, high, close, adj_close = row[:7]
                    date = parse_date(date_str)
                    if not date:
                        continue

                    stock_data = StockData(
                        market=file_name.split('/')[1],
                        ticker=file_name.split('/')[3].replace('.csv', ''),
                        open_price=parse_double(open_price),
                        high=parse_double(high),
                        low=parse_double(low),
                        close=parse_double(close),
                        volume=parse_double(volume),
                        adj_close=parse_double(adj_close)
                    )
                    
                    records.append(stock_data)
                    if len(records) >= n:
                        break

            files.remove(file_name)  # Remove the file to avoid repeated access

    return records[:n]  # Return only n records

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key.low < arr[j].low:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def iterative_quicksort(arr):
    stack = [(0, len(arr) - 1)]
    
    while stack:
        low, high = stack.pop()
        
        if low < high:
            pi = partition(arr, low, high)
            stack.append((low, pi - 1))
            stack.append((pi + 1, high))

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j].low <= pivot.low:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i].low < right_half[j].low:
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

def run_and_time_sorting(sort_func, data):
    start_time = time.time()
    sort_func(data)
    return time.time() - start_time

def empirical_analysis(zip_file_path, n, sort_func):
    if n <= 0:
        print("Requested size must be greater than 0.")
        return

    # Read random n records from the zip file (once)
    sample_data = read_random_records(zip_file_path, n)

    # Perform 5 runs on presorted and not presorted data
    presorted_times = []
    not_presorted_times = []

    for _ in range(5):
        # Presorted data: Sort first, then time the sort
        sorted_data = sorted(sample_data, key=lambda x: x.low)  # Presort
        presorted_times.append(run_and_time_sorting(sort_func, sorted_data.copy()))

        # Not presorted: Shuffle, then time the sort
        random.shuffle(sample_data)
        not_presorted_times.append(run_and_time_sorting(sort_func, sample_data.copy()))

    # Calculate average times
    avg_presorted_time = sum(presorted_times) / 5
    avg_not_presorted_time = sum(not_presorted_times) / 5

    print(f"Sorting completed:")
    print(f"Average presorted time: {avg_presorted_time:.4f} seconds")
    print(f"Average not presorted time: {avg_not_presorted_time:.4f} seconds")

# Main Execution
if __name__ == "__main__":
    zip_file_path = "C:\\cygwin64\\home\\tommy\\322hw\\archive.zip"
    while True:
        user_input = input("Enter dataset size (n) and sorting algorithm (i for Insertion, q for QuickSort, m for Merge Sort), or type 'quit' to exit: ").strip()
        if user_input.lower() == 'quit':
            break

        try:
            n_str, algo = user_input.split()
            n = int(n_str)

            # Determine the sorting algorithm
            if algo == 'i':
                sort_func = insertion_sort
            elif algo == 'q':
                sort_func = iterative_quicksort
            elif algo == 'm':
                sort_func = merge_sort
            else:
                print("Invalid sorting algorithm specified.")
                continue

            empirical_analysis(zip_file_path, n, sort_func)

        except ValueError:
            print("Invalid input. Please enter in the format: <n> <sort_algo>")
