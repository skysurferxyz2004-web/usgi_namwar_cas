# U.S. Military Casualty Data Visualization

"""
This script fetches U.S. military casualty data from
https://www.archives.gov/research/military/vietnam-war/casualty-statistics
and visualizes it as a chart using matplotlib.
"""
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

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
    x = np.arange(len(labels))
    y = np.zeros_like(x)  # All bars at y=0
    z = np.zeros_like(x)  # All bars start at z=0
    dx = np.ones_like(x) * 0.6  # Bar width
    dy = np.ones_like(x) * 0.6  # Bar depth
    dz = np.array(values)        # Bar height

    fig = plt.figure(figsize=(14, 7))
    ax = fig.add_subplot(111, projection='3d')

    # 3D bar plot
    ax.bar3d(x, y, z, dx, dy, dz, color='#00bfff', alpha=0.85, edgecolor='k', linewidth=0.5)

    # Set labels and title
    ax.set_title('U.S. Military Casualties (Vietnam War, 3D Histogram)', fontsize=20, color='#FFD700', pad=20)
    ax.set_xlabel('Category', fontsize=14, color='#FFD700')
    ax.set_ylabel('Y', fontsize=14, color='#FFD700')
    ax.set_zlabel('Number of Casualties', fontsize=14, color='#FFD700')

    # Set x-ticks as labels
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right', color='#FFD700')
    ax.set_yticks([])  # Hide y-ticks for clarity

    # Artistic tweaks: color ticks and labels (Axes3D doesn't expose w_xaxis)
    ax.tick_params(axis='x', colors='#FFD700', labelrotation=45)
    ax.tick_params(axis='y', colors='#FFD700')
    ax.tick_params(axis='z', colors='#FFD700')
    for lbl in ax.get_xticklabels():
        lbl.set_color('#FFD700')
    for lbl in ax.get_yticklabels():
        lbl.set_color('#FFD700')
    for lbl in ax.get_zticklabels():
        lbl.set_color('#FFD700')
    ax.grid(color='#444444', linestyle='--', linewidth=0.7, alpha=0.5)
    fig.patch.set_facecolor('#222222')
    ax.set_facecolor('#222222')

    # Watermark
    fig.text(0.5, 0.02, 'semper fidelis', fontsize=24, color='#444444', ha='center', alpha=0.3, style='italic')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    url = 'https://www.archives.gov/research/military/vietnam-war/casualty-statistics'
    data = fetch_casualty_data(url)
    if data:
        plot_casualty_chart(data)
    else:
        print('No data found or unable to parse the table.')
