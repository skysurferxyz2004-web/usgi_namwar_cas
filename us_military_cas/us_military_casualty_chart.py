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
    dx = np.ones_like(x) * 0.75  # Bar width
    dy = np.ones_like(x) * 0.6   # Bar depth
    dz = np.array(values)        # Bar height

    # Figure and axes with dark theme
    fig = plt.figure(figsize=(16, 9), facecolor='#0b0b0b')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#0b0b0b')

    # Color map based on height to give a gradient feel
    cmap = plt.get_cmap('magma')
    norm = plt.Normalize(dz.min() if dz.size else 0, dz.max() if dz.size else 1)
    colors = cmap(norm(dz))

    # Soft shadow behind bars (slightly offset, dark translucent)
    ax.bar3d(x - 0.06, y - 0.06, z, dx, dy, dz * 0.98, color='black', alpha=0.12, zsort='average')

    # Main bars with color mapping and black edges for contrast
    ax.bar3d(x, y, z, dx, dy, dz, color=colors, edgecolor='black', linewidth=0.6, zsort='average')

    # Title and subtitle styling
    ax.set_title('U.S. Military Casualties — 3D Histogram', fontsize=24, color='#ffd966', pad=20)
    fig.text(0.06, 0.93, 'Data source: archives.gov — rendered with artistic styling', color='#cccccc', fontsize=10)

    # Axes labels
    ax.set_xlabel('Category', fontsize=14, color='#ffd966', labelpad=10)
    ax.set_ylabel('Depth', fontsize=14, color='#ffd966', labelpad=10)
    ax.set_zlabel('Number of Casualties', fontsize=14, color='#ffd966', labelpad=6)

    # X ticks and label handling (avoid clutter for many categories)
    ax.set_xticks(x)
    max_labels = 20
    if len(labels) > max_labels:
        # show a subset of labels to keep the plot readable
        step = max(1, len(labels) // max_labels)
        tick_pos = x[::step]
        tick_labels = [labels[i] for i in range(0, len(labels), step)]
        ax.set_xticks(tick_pos)
        ax.set_xticklabels(tick_labels, rotation=30, ha='right', color='#ffd966', fontsize=9)
    else:
        ax.set_xticklabels(labels, rotation=30, ha='right', color='#ffd966', fontsize=10)
    ax.set_yticks([])

    # Annotate bar tops with values and highlight top-3 bars
    if dz.size:
        top_n = 3
        top_idx = dz.argsort()[-top_n:][::-1]
        max_z = dz.max()
        for i, (xi, zi) in enumerate(zip(x, dz)):
            # numeric label above each bar
            ax.text(xi + dx[i] / 2, 0, zi + max_z * 0.02, f'{int(zi):,}', color='#ffe6a7',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
        # add a small marker for the top bars
        for idx in top_idx:
            ax.text(x[idx] + dx[idx] / 2, 0, dz[idx] + max_z * 0.07, '★', color='#ff6f61',
                    ha='center', va='bottom', fontsize=18)

    # Subtle grid using projected lines (keep low-contrast)
    ax.xaxis._axinfo['grid']['color'] = '#222222'
    ax.yaxis._axinfo['grid']['color'] = '#222222'
    ax.zaxis._axinfo['grid']['color'] = '#222222'

    # Tick colors
    for lbl in ax.get_xticklabels():
        lbl.set_color('#ffd966')
    for lbl in ax.get_yticklabels():
        lbl.set_color('#ffd966')
    for lbl in ax.get_zticklabels():
        lbl.set_color('#ffd966')

    # Camera angle for a more dramatic view
    ax.view_init(elev=28, azim=-60)

    # Watermark
    fig.text(0.5, 0.02, 'semper fidelis', fontsize=28, color='#444444', ha='center', alpha=0.25, style='italic')

    # Tight layout with slightly expanded margins to avoid overlap
    plt.subplots_adjust(left=0.06, right=0.98, top=0.88, bottom=0.12)
    plt.show()

if __name__ == '__main__':
    url = 'https://www.archives.gov/research/military/vietnam-war/casualty-statistics'
    data = fetch_casualty_data(url)
    if data:
        plot_casualty_chart(data)
    else:
        print('No data found or unable to parse the table.')
