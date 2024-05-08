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

# Function to plot daily total number of flights as a background column graph
def plot_daily_flights(ax, df):
    daily_flights = df.resample('D', on='Flight Date').size()
    ax.bar(daily_flights.index, daily_flights.values, width=0.8, color='lightblue', alpha=0.7)
    ax.set_ylabel('Number of Flights')

# Plotting for Aircraft starting with "Aero"
aero_data = filter_aircraft_by_prefix(data_filtered, "Aero")
plt.figure(figsize=(12, 6))

# Plot background column graph for daily total number of flights
ax = plt.gca()
plot_daily_flights(ax, aero_data)

# Plot cumulative distance for each aircraft
for aircraft, df in aero_data.groupby('Drone Name'):
    cumulative_distance = calculate_cumulative_distance(df)
    plt.plot(cumulative_distance.index, cumulative_distance.values, label=aircraft)

plt.xlabel('Date')
plt.ylabel('Cumulative Distance (km)')
plt.title('Aircraft Starting with "Aero"')
plt.legend(loc="upper left")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Plotting for Aircraft starting with "Bullet 2.1"
bullet_data = filter_aircraft_by_prefix(data_filtered, "Bullet 2.1")
plt.figure(figsize=(12, 6))

# Plot background column graph for daily total number of flights
ax = plt.gca()
plot_daily_flights(ax, bullet_data)

# Plot cumulative distance for each aircraft
for aircraft, df in bullet_data.groupby('Drone Name'):
    cumulative_distance = calculate_cumulative_distance(df)
    plt.plot(cumulative_distance.index, cumulative_distance.values, label=aircraft)

plt.xlabel('Date')
plt.ylabel('Cumulative Distance (km)')
plt.title('Aircraft Starting with "Bullet 2.1"')
plt.legend(loc="upper left")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Plotting for Aircraft starting with "Fighter"
fighter_data = filter_aircraft_by_prefix(data_filtered, "Fighter")
plt.figure(figsize=(12, 6))

# Plot background column graph for daily total number of flights
ax = plt.gca()
plot_daily_flights(ax, fighter_data)

# Plot cumulative distance for each aircraft
for aircraft, df in fighter_data.groupby('Drone Name'):
    cumulative_distance = calculate_cumulative_distance(df)
    plt.plot(cumulative_distance.index, cumulative_distance.values, label=aircraft)

plt.xlabel('Date')
plt.ylabel('Cumulative Distance (km)')
plt.title('Aircraft Starting with "Fighter"')
plt.legend(loc="upper left")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Show all plots
plt.show()
