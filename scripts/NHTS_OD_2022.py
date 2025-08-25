import pandas
import matplotlib.pyplot as plt

def get_aggregated_trips_by_distance_mode():
    df = pandas.read_csv("datasets/NHTS_OD_2022/2022_Passenger_OD_Annual/2022_Passenger_OD_Annual_Data.csv")
    
    
    distance_fields = ['_0_10mi', '_10_25mi', '_25_50mi', '_50_75mi', '_75_100mi', '_100_150mi', '_150_300mi', '_gt300mi']

    output_df = df.groupby(['mode']).agg({col: 'sum' for col in distance_fields}).reset_index()
    return output_df