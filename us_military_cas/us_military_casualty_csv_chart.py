# U.S. Military Casualty Data Visualization from CSV

"""
This script reads U.S. military casualty data from a CSV file where each line contains a datetime and a float separated by a comma, and visualizes it as a chart using matplotlib.
"""
import matplotlib.pyplot as plt
import csv
from datetime import datetime

CSV_FILE = 'casualty_data.csv'  # Update this filename if needed

def read_csv_data(filename):
    dates = []
    values = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 2:
                continue
            try:
                date = datetime.fromisoformat(row[0])
                value = float(row[1])
                dates.append(date)
                values.append(value)
            except Exception:
                continue
    return dates, values

def plot_casualty_chart(dates, values):
    plt.figure(figsize=(12, 6))
    plt.plot(dates, values, marker='o', linestyle='-', color='navy')
    plt.title('U.S. Military Casualties Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Casualties')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    dates, values = read_csv_data(CSV_FILE)
    if dates and values:
        plot_casualty_chart(dates, values)
    else:
        print('No valid data found in CSV file.')
