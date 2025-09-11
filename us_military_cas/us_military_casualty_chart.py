# U.S. Military Casualty Data Visualization

"""
This script fetches U.S. military casualty data from
https://www.archives.gov/research/military/vietnam-war/casualty-statistics
and visualizes it as a chart using matplotlib.
"""
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# Fetch data from the website
def fetch_casualty_data(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    # Example: Find the relevant table
    tables = soup.find_all('table')
    data = []
    # Try to parse the first table for demonstration
    if tables:
        table = tables[0]
        for row in table.find_all('tr')[1:]:
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 2:
                label = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                try:
                    value = int(value.replace(',', ''))
                except ValueError:
                    continue
                data.append((label, value))
    return data

def plot_casualty_chart(data):
    labels, values = zip(*data)
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='navy')
    plt.title('U.S. Military Casualties (Vietnam War)')
    plt.xlabel('Category')
    plt.ylabel('Number of Casualties')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    url = 'https://www.archives.gov/research/military/vietnam-war/casualty-statistics'
    data = fetch_casualty_data(url)
    if data:
        plot_casualty_chart(data)
    else:
        print('No data found or unable to parse the table.')
