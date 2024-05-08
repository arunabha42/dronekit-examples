import pandas as pd

# Load the dataset
data = pd.read_csv('DLB-Flights-May2021-May2024.csv')

# Get the number of rows
num_rows = data.shape[0]

print("Number of rows in the dataset:", num_rows)
