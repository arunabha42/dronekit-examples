import math

def calculate_heading(lat1, lon1, lat2, lon2):
    # Convert decimal degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    # Calculate the difference between the longitudes
    delta_lon = lon2 - lon1
    
    # Calculate the heading
    y = math.sin(delta_lon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
    heading = math.atan2(y, x)
    
    # Convert heading from radians to degrees
    heading = round(math.degrees(heading))
    
    # Normalize the heading to be in the range [0, 360]
    heading = (heading + 360) % 360
    
    return heading

# Example coordinates
lat1 = float(input("Enter latitude of the first point (in decimal degrees): "))
lon1 = float(input("Enter longitude of the first point (in decimal degrees): "))
lat2 = float(input("Enter latitude of the second point (in decimal degrees): "))
lon2 = float(input("Enter longitude of the second point (in decimal degrees): "))

# Calculate heading
heading = calculate_heading(lat1, lon1, lat2, lon2)
print("Heading from the first point to the second point:", heading, "degrees")
