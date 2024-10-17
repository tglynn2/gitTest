#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zlib.h>
#include <time.h>

#define MAX_LINE_LENGTH 1024
#define INITIAL_MAX_STOCKS 1000

typedef struct {
    char market[50];
    char ticker[50];
    double open_price;
    double high;
    double low;
    double close;
    double volume;
    double adj_close;
} StockData;

typedef struct {
    char key[100];
    StockData stock_data;
} StockEntry;

typedef struct {
    int day;
    int month;
    int year;
} Date;

typedef struct {
    Date date;
    StockEntry *stocks;   // Dynamically allocate
    int stock_count;
    int max_stocks;
} DateStockData;

DateStockData *stock_data_by_date = NULL;  // Dynamically allocate
int date_stock_data_count = 0;
int max_date_stock_data = INITIAL_MAX_STOCKS;  // Initial capacity

int parse_date(const char *date_str, Date *date) {
    return sscanf(date_str, "%d-%d-%d", &date->day, &date->month, &date->year);
}

double parse_double(const char *value) {
    if (value == NULL || strlen(value) == 0) return 0.0;
    return strtod(value, NULL);
}

void read_zip_data(const char *zip_file_path) {
    gzFile zfile = gzopen(zip_file_path, "rb");
    if (!zfile) {
        fprintf(stderr, "Error opening zip file\n");
        return;
    }

    char buffer[MAX_LINE_LENGTH];
    while (gzgets(zfile, buffer, MAX_LINE_LENGTH)) {
        char date_str[20], low[20], open_price[20], volume[20], high[20], close[20], adj_close[20];
        sscanf(buffer, "%[^,],%[^,],%[^,],%[^,],%[^,],%[^,],%s",
               date_str, low, open_price, volume, high, close, adj_close);

        Date date;
        if (!parse_date(date_str, &date)) {
            fprintf(stderr, "Error parsing date: %s\n", date_str);
            continue;
        }

        StockData stock_data;
        strcpy(stock_data.market, "MockMarket");
        strcpy(stock_data.ticker, "MockTicker");
        stock_data.open_price = parse_double(open_price);
        stock_data.high = parse_double(high);
        stock_data.low = parse_double(low);
        stock_data.close = parse_double(close);
        stock_data.volume = parse_double(volume);
        stock_data.adj_close = parse_double(adj_close);

        int found = 0;
        for (int i = 0; i < date_stock_data_count; ++i) {
            if (stock_data_by_date[i].date.day == date.day &&
                stock_data_by_date[i].date.month == date.month &&
                stock_data_by_date[i].date.year == date.year) {
                // Add stock to existing date entry
                if (stock_data_by_date[i].stock_count >= stock_data_by_date[i].max_stocks) {
                    stock_data_by_date[i].max_stocks *= 2;
                    stock_data_by_date[i].stocks = realloc(stock_data_by_date[i].stocks, stock_data_by_date[i].max_stocks * sizeof(StockEntry));
                }
                stock_data_by_date[i].stocks[stock_data_by_date[i].stock_count++] = (StockEntry){"MockTicker", stock_data};
                found = 1;
                break;
            }
        }

        if (!found) {
            if (date_stock_data_count >= max_date_stock_data) {
                max_date_stock_data *= 2;
                stock_data_by_date = realloc(stock_data_by_date, max_date_stock_data * sizeof(DateStockData));
            }
            DateStockData new_date_stock_data;
            new_date_stock_data.date = date;
            new_date_stock_data.stock_count = 0;
            new_date_stock_data.max_stocks = INITIAL_MAX_STOCKS;
            new_date_stock_data.stocks = malloc(INITIAL_MAX_STOCKS * sizeof(StockEntry));
            new_date_stock_data.stocks[new_date_stock_data.stock_count++] = (StockEntry){"MockTicker", stock_data};
            stock_data_by_date[date_stock_data_count++] = new_date_stock_data;
        }
    }

    gzclose(zfile);
}

int compare_dates(const Date *a, const Date *b) {
    if (a->year != b->year) return a->year - b->year;
    if (a->month != b->month) return a->month - b->month;
    return a->day - b->day;
}

int partition(DateStockData arr[], int low, int high) {
    DateStockData pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; ++j) {
        if (compare_dates(&arr[j].date, &pivot.date) <= 0) {
            i++;
            DateStockData temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    DateStockData temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;
    return i + 1;
}

void quicksort(DateStockData arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quicksort(arr, low, pi - 1);
        quicksort(arr, pi + 1, high);
    }
}

void write_avg_data_to_csv(const char *output_file) {
    FILE *file = fopen(output_file, "w");
    if (!file) {
        fprintf(stderr, "Error opening file for writing\n");
        return;
    }

    fprintf(file, "Ticker,Market,Lowest,Highest,AverageVolume,Period\n");

    for (int i = 0; i < date_stock_data_count; ++i) {
        for (int j = 0; j < stock_data_by_date[i].stock_count; ++j) {
            StockData *stock = &stock_data_by_date[i].stocks[j].stock_data;
            fprintf(file, "%s,%s,%.2f,%.2f,%.2f,%02d-%02d-%d to %02d-%02d-%d\n",
                    stock_data_by_date[i].stocks[j].key,
                    stock->market,
                    stock->low,
                    stock->high,
                    stock->volume,
                    stock_data_by_date[i].date.day,
                    stock_data_by_date[i].date.month,
                    stock_data_by_date[i].date.year,
                    stock_data_by_date[0].date.day,
                    stock_data_by_date[0].date.month,
                    stock_data_by_date[0].date.year);
        }
    }

    fclose(file);
}

void write_sorted_data_to_csv(const char *output_file) {
    quicksort(stock_data_by_date, 0, date_stock_data_count - 1);

    FILE *file = fopen(output_file, "w");
    if (!file) {
        fprintf(stderr, "Error opening file for writing\n");
        return;
    }

    for (int i = 0; i < date_stock_data_count; ++i) {
        fprintf(file, "%02d-%02d-%d: ",
                stock_data_by_date[i].date.day,
                stock_data_by_date[i].date.month,
                stock_data_by_date[i].date.year);

        for (int j = 0; j < stock_data_by_date[i].stock_count; ++j) {
            fprintf(file, "%s ", stock_data_by_date[i].stocks[j].key);
        }
        fprintf(file, "\n");
    }

    fclose(file);
}

int main() {
    stock_data_by_date = malloc(INITIAL_MAX_STOCKS * sizeof(DateStockData));

    const char *zip_file_path = "C:\cygwin64\home\tommy\322hw\archive.zip";
    read_zip_data(zip_file_path);

    const char *avg_output_file = "C:\cygwin64\home\tommy\322hw\averagesC.csv";
    write_avg_data_to_csv(avg_output_file);

    const char *sorted_output_file = "C:\cygwin64\home\tommy\322hw\sortedC.csv";
    write_sorted_data_to_csv(sorted_output_file);

    for (int i = 0; i < date_stock_data_count; ++i) {
        free(stock_data_by_date[i].stocks);
    }
    free(stock_data_by_date);

    return 0;
}


