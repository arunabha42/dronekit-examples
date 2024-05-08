import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('DLB-Flights-May2021-May2024.csv')

# Convert 'Flight Date' to datetime format
data['Flight Date'] = pd.to_datetime(data['Flight Date'])

# Filter out specified drone names
drone_names_to_exclude = ['Bullet 2.1 SITL', 'Mugin-1', 'RQ 850 30mm', 'RQ 850 v2.3']
data_filtered = data[~data['Drone Name'].isin(drone_names_to_exclude)]

# Define function to filter aircraft by name starting with specific prefixes
def filter_aircraft_by_prefix(data, prefix):
    return data[data['Drone Name'].str.startswith(prefix)]

# Function to calculate cumulative distance for each aircraft in kilometers (rounded off)
def calculate_cumulative_distance(df):
    return (df.groupby('Flight Date')['Travelled Distance ( m)'].sum() / 1000).round().cumsum()

# Plotting
plt.figure(figsize=(12, 6))

# Filter data for each group
incident_human_error = data_filtered[data_filtered['Drone Name'].isin(['Bullet 2.1 Delta', 'Bullet 2.1 Foxtrot', 'Bullet 2.1 Hotel'])]
incident_technical_error = data_filtered[data_filtered['Drone Name'].isin(['AeroSwift AS01', 'Bullet 2.1 Alpha', 'Bullet 2.1 Bravo', 'Bullet 2.1 Golf', 'Fighter A', 'Fighter C', 'Fighter E'])]
retired = data_filtered[data_filtered['Drone Name'].isin(['Bullet 2.0 Alpha', 'Bullet 2.0 Bravo'])]
in_service = data_filtered[~data_filtered['Drone Name'].isin(incident_human_error['Drone Name'].tolist() + incident_technical_error['Drone Name'].tolist() + retired['Drone Name'].tolist())]

# Plot cumulative distance for each group
for group, color, label in zip([incident_human_error, incident_technical_error, retired, in_service],
                                ['orange', 'yellow', 'gray', 'green'],
                                ['Incident - Human Error', 'Incident - Technical Error', 'Retired', 'In Service']):
    cumulative_distance = calculate_cumulative_distance(group)
    plt.plot(cumulative_distance.index, cumulative_distance.values, color=color, label=label)

plt.xlabel('Date')
plt.ylabel('Cumulative Distance (km)')
plt.title('Cumulative Distance Traveled by Aircraft')
plt.legend(loc='upper left')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()
