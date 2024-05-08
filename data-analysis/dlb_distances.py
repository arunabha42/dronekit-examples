import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('DLB-Flights-May2021-May2024.csv')

# Convert 'Flight Date' to datetime format
data['Flight Date'] = pd.to_datetime(data['Flight Date'])

# Filter out specified drone names
drone_names_to_exclude = ['Bullet 2.1 SITL', 'Mugin-1', 'RQ 850 30mm', 'RQ 850 v2.3']
data_filtered = data[~data['Drone Name'].isin(drone_names_to_exclude)]

# Group by aircraft name and flight date, then sum up the distances
aircraft_distances = data_filtered.groupby(['Drone Name', 'Flight Date'])['Travelled Distance ( m)'].sum().reset_index()

# Ask user for the number of rows in the dataset to use
num_rows_input = input("Enter the number of rows in the dataset to use (press Enter for all rows): ")

# Check if user input is empty (i.e., Enter key pressed)
if num_rows_input.strip() == "":
    num_rows = len(aircraft_distances)
else:
    num_rows = int(num_rows_input)

# Limit the dataset to the specified number of rows
limited_data = aircraft_distances.head(num_rows)

# Calculate cumulative distance for each aircraft in kilometers (rounded to nearest whole number)
cumulative_distances_km = (limited_data.groupby('Drone Name')['Travelled Distance ( m)'].cumsum() / 1000).round()

# Plotting
plt.figure(figsize=(10, 6))

# Iterate over each aircraft
for aircraft, df in limited_data.groupby('Drone Name'):
    plt.plot(df['Flight Date'], cumulative_distances_km[df.index], label=aircraft)

# Customize plot
plt.xlabel('Date')
plt.ylabel('Cumulative Distance (km)')
plt.title(f'Cumulative Distance Traveled by Aircraft (First {num_rows} Rows)')
plt.legend(loc="upper left")  # Specify legend location
plt.grid(True)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show plot
plt.tight_layout()
plt.show()
