import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("DLB-Flights-May2021-May2024.csv")

# Convert 'Flight Date' to datetime format
df['Flight Date'] = pd.to_datetime(df['Flight Date'])

# Extracting date from 'Flight Date' to group by
df['Date'] = df['Flight Date'].dt.date

# Group by date and calculate the cumulative distance travelled and number of flights per day
daily_stats = df.groupby('Date').agg({'Travelled Distance ( m)': 'sum', 'flightGUID': 'count'}).reset_index()
daily_stats.columns = ['Date', 'Cumulative Distance (km)', 'Number of Flights']

# Convert distance from meters to kilometers
daily_stats['Cumulative Distance (km)'] = daily_stats['Cumulative Distance (km)'] / 1000

# Calculate cumulative sum of distance travelled
daily_stats['Cumulative Distance (km)'] = daily_stats['Cumulative Distance (km)'].cumsum()

# Plotting
plt.figure(figsize=(12, 6))

# Plotting cumulative distance travelled
plt.plot(daily_stats['Date'], daily_stats['Cumulative Distance (km)'], color='b', label='Cumulative Distance')
plt.ylabel('Cumulative Distance (km)')

# Create a secondary y-axis for daily number of flights
plt.twinx()

# Plotting daily number of flights with increased width of bars
plt.bar(daily_stats['Date'], daily_stats['Number of Flights'], color='g', alpha=0.6, label='Daily Number of Flights', width=0.8)
plt.ylabel('Number of Flights')

# Adding labels and title
plt.title('Flight Data Analysis')
plt.xlabel('Date')

# Adding legend for both plots
plt.legend(loc='upper left')

# Adding grid
plt.grid(True)

plt.show()
