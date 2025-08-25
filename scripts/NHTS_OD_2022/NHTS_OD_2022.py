import pandas
import matplotlib.pyplot as plt
import numpy as np

mode_fields = ['air', 'rail', 'vehicle', 'atf'] # atf = active (walk, bike, ferry)
distance_fields = ['_0_10mi', '_10_25mi', '_25_50mi', '_50_75mi', '_75_100mi', '_100_150mi', '_150_300mi', '_gt300mi']
distance_fields_pretty = ['0 to 10 miles', '10 to 25 miles', '25 to 50 miles', '50 to 75 miles', '75 to 100 miles', '100 to 150 miles', '150 to 300 miles', '>300 miles']

fields = [f"{mode}{distance}" for mode in mode_fields for distance in distance_fields]

save_dir = "scripts/NHTS_OD_2022/"
show = False  # Set to False to skip showing plots

def get_aggregated_trips_by_distance_mode():
    """Get aggregated trips by distance and mode.

    Field names are constructed as "{mode}{distance}" for each combination of mode and distance. Eg. "air_0_10mi"

    Returns:
        dataframe: A dataframe of key field string (mode, distance) and data sum of trips
    """
    
    df = pandas.read_csv("datasets/NHTS_OD_2022/2022_Passenger_OD_Annual/2022_Passenger_OD_Annual_Data.csv")
    
    aggregated_trips = {}
    for field in fields:
        aggregated_trips[field] = df[field].sum()

    return aggregated_trips

def plot_aggregated_trips_by_distance_mode(aggregated_trips):
    plt.figure(figsize=(12.8, 7.2), dpi=100)  # 1280x720 pixels at 100 DPI
    labels = mode_fields
    
    values = []
    for distance_field in distance_fields:
        values.append([aggregated_trips.get(f"{mode}{distance_field}", 0) for mode in mode_fields])

    bottom = np.zeros(len(labels))
    for i, value in enumerate(values):
        plt.bar(labels,
                value, # Value is the list of trips by mode for a given distance (eg. 10 air 0-10 miles, 50 car 0-10 miles)
                bottom=bottom,
                label=distance_fields_pretty[i]
                )
        bottom += np.array(value) # Increase start point for the next bar
        
    plt.title('Trips by Mode and Distance')
    plt.xlabel('Transportation Mode')
    plt.ylabel('Number of Trips')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(f'{save_dir}trips_by_mode_distance.png', dpi=100, bbox_inches='tight')
    print(f"Plot saved as '{save_dir}trips_by_mode_distance.png'")
    if show:
        plt.show()
    else:
        plt.close()

def save_aggregated_trips_csv(aggregated_trips):
    # Create a DataFrame with distances as rows and modes as columns
    data = {}
    for mode in mode_fields:
        data[mode] = []
        for distance_field in distance_fields:
            key = f"{mode}{distance_field}"
            data[mode].append(aggregated_trips.get(key, 0))
    
    df = pandas.DataFrame(data, index=distance_fields_pretty)
    df.index.name = 'Distance'
    df.to_csv(f'{save_dir}aggregated_trips.csv')
    print(f"CSV saved as '{save_dir}aggregated_trips.csv'")

def plot_pie_charts_by_mode(aggregated_trips):
    """Generate separate pie charts for each mode."""
    mode_names = {'air': 'Air', 'rail': 'Rail', 'vehicle': 'Vehicle', 'atf': 'Active'}
    
    for mode in mode_fields:
        trips = [aggregated_trips.get(f"{mode}{dist}", 0) for dist in distance_fields]
        nonzero_trips = [t for t in trips if t > 0]
        nonzero_labels = [distance_fields_pretty[i] for i, t in enumerate(trips) if t > 0]
        
        if nonzero_trips:
            plt.figure(figsize=(12, 8))
            wedges, texts, autotexts = plt.pie(nonzero_trips, autopct='%1.1f%%', startangle=90)
            plt.legend(wedges, nonzero_labels, title="Distance Ranges", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            plt.title(f'{mode_names[mode]} - Total: {sum(nonzero_trips):,} trips')
            plt.savefig(f'{save_dir}pie_{mode}.png', dpi=100, bbox_inches='tight')
            print(f"Pie chart saved as '{save_dir}pie_{mode}.png'")
            if show:
                plt.show()
            else:
                plt.close()

def check_row_sum():
    # For each row, sum only the mode+distance fields and check if it matches the total trips field. If it doesn't, increment a counter
    df = pandas.read_csv('datasets/NHTS_OD_2022/2022_Passenger_OD_Annual/2022_Passenger_OD_Annual_Data.csv')
    total_mismatches = 0
    for index, row in df.iterrows():
        row_sum = row[fields].sum()
        if row_sum != row['annual_total_trips']:
            total_mismatches += 1
    print(f"Total mismatches found: {total_mismatches}")

aggregated_trips = get_aggregated_trips_by_distance_mode()
plot_aggregated_trips_by_distance_mode(aggregated_trips)
plot_pie_charts_by_mode(aggregated_trips)
save_aggregated_trips_csv(aggregated_trips)

#check_row_sum() # 0 mismatches found!