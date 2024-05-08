import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('DLB-Flights-May2021-May2024.csv')

# Convert 'Flight Date' to datetime format
data['Flight Date'] = pd.to_datetime(data['Flight Date'])

# Filter out specified drone names
drone_names_to_exclude = ['Bullet 2.1 SITL', 'Mugin-1', 'RQ 850 30mm', 'RQ 850 v2.3']
data_filtered = data[~data['Drone Name'].isin(drone_names_to_exclude)]

# Define functions to filter aircraft by name starting with specific prefixes
def filter_aircraft_by_prefix(data, prefix):
    return data[data['Drone Name'].str.startswith(prefix)]

# Function to calculate cumulative distance for each aircraft in kilometers (rounded off)
def calculate_cumulative_distance(df):
    return (df.groupby('Flight Date')['Travelled Distance ( m)'].sum() / 1000).round().cumsum()

# Plotting for all aircraft
plt.figure(figsize=(12, 6))

# Filtered data without excluded drone names
filtered_data = data_filtered[~data_filtered['Drone Name'].isin(drone_names_to_exclude)]

# Filtered data for specific aircraft with red lines
red_aircraft = filtered_data[filtered_data['Drone Name'].isin([
    'AeroSwift AS01',
    'Bullet 2.0 Alpha',
    'Bullet 2.0 Bravo',
    'Bullet 2.1 Alpha',
    'Bullet 2.1 Bravo',
    'Bullet 2.1 Delta',
    'Bullet 2.1 Echo',
    'Bullet 2.1 Foxtrot',
    'Bullet 2.1 Golf',
    'Bullet 2.1 Hotel',
    'Fighter A',
    'Fighter C',
    'Fighter E'
])]

# Plot cumulative distance for each red aircraft
for aircraft, df in red_aircraft.groupby('Drone Name'):
    cumulative_distance = calculate_cumulative_distance(df)
    plt.plot(cumulative_distance.index, cumulative_distance.values, color='red')

# Filtered data for other aircraft with green lines
green_aircraft = filtered_data[~filtered_data['Drone Name'].isin(red_aircraft['Drone Name'])]

# Plot cumulative distance for each green aircraft
for aircraft, df in green_aircraft.groupby('Drone Name'):
    cumulative_distance = calculate_cumulative_distance(df)
    plt.plot(cumulative_distance.index, cumulative_distance.values, color='green')

plt.xlabel('Date')
plt.ylabel('Cumulative Distance (km)')
plt.title('Cumulative Distance Traveled by Aircraft')

# Customize legend
# plt.legend(['In Service', 'Decommissioned'], loc='upper left')

# Create custom legend handles
legend_handles = [plt.Line2D([0], [0], color='green', lw=2),
                  plt.Line2D([0], [0], color='red', lw=2)]

# Create the legend
plt.legend(legend_handles, ['In Service', 'Decommissioned'], loc='upper left')

plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()
