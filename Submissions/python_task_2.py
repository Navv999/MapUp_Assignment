import pandas as pd
import networkx as nx
import time
from datetime import datetime, timedelta, time



def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    # Create a directed graph
   # Read the dataset into a DataFrame

    # 
    # Create an empty distance matrix with unique IDs
    unique_ids = sorted(set(df['id_start'].tolist() + df['id_end'].tolist()))
    distance_matrix = pd.DataFrame(index=unique_ids, columns=unique_ids).fillna(0)

    # Update the distance matrix with cumulative distances
    for index, row in df.iterrows():
        id_start, id_end, distance = row['id_start'], row['id_end'], row['distance']
        distance_matrix.loc[id_start, id_end] += distance
        distance_matrix.loc[id_end, id_start] += distance  # Accounting for bidirectional distances

    return distance_matrix


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
     # Reset the index to make id_start and id_end as regular columns
    # Create an empty DataFrame to store unrolled data
   # Create an empty list to store unrolled data
    unrolled_data = []

    # Iterate over rows and columns of the distance matrix
    for i in dist_mat.index:
        for j in dist_mat.columns:
            # Skip same 'id_start' to 'id_end' combinations
            if i != j:
                unrolled_data.append({
                    'id_start': i,
                    'id_end': j,
                    'distance': dist_mat.loc[i, j]
                })

    # Create a DataFrame from the list of dictionaries
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df

    return df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
     # Filter DataFrame for the given reference_id
    reference_df = df[df['id_start'] == reference_id]

    # Calculate the average distance for the reference_id
    reference_avg_distance = reference_df['distance'].mean()

    # Calculate the threshold range (10% of the average distance)
    threshold_lower = reference_avg_distance * 0.9
    threshold_upper = reference_avg_distance * 1.1

    # Filter DataFrame for IDs within the threshold range
    result_df = df[(df['id_start'] != reference_id) & 
                   (df['distance'] >= threshold_lower) & 
                   (df['distance'] <= threshold_upper)]

    # Sort the result DataFrame by 'id_start'
    result_df = result_df.sort_values(by='id_start')

    return result_df


    return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    # Rate coefficients for each vehicle type
    rate_coefficients = {
        'moto': 0.05,
        'car': 0.1,
        'rv': 0.2,
        'bus': 0.3,
        'truck': 0.4
    }

    # Calculate toll rates for each vehicle type
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df

    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    # Define time ranges for weekdays and weekends
    weekday_time_ranges = [(time(0, 0, 0), time(10, 0, 0)),
                           (time(10, 0, 0), time(18, 0, 0)),
                           (time(18, 0, 0), time(23, 59, 59))]
    
    weekend_time_ranges = [(time(0, 0, 0), time(23, 59, 59))]

    # Initialize an empty DataFrame to store the result
    result_df = pd.DataFrame()

    # Iterate over unique (id_start, id_end) pairs
    for _, group in df.groupby(['id_start', 'id_end']):
        id_start, id_end = group.iloc[0]['id_start'], group.iloc[0]['id_end']

        # Iterate over days of the week
        for day in range(7):
            start_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            start_day += timedelta(days=day)
            
            end_day = start_day.replace(hour=23, minute=59, second=59)

            # Iterate over time ranges based on weekdays or weekends
            time_ranges = weekday_time_ranges if day < 5 else weekend_time_ranges

            for start_time, end_time in time_ranges:
                start_datetime = datetime.combine(start_day, start_time)
                end_datetime = datetime.combine(end_day, end_time)

                # Apply discount factors based on time range
                discount_factor = 0.8 if start_time < time(10, 0, 0) or (start_time >= time(18, 0, 0) and start_time <= time(23, 59, 59)) else 1.2
                group_copy = group.copy()
                group_copy['start_day'] = start_day.strftime('%A')
                group_copy['start_time'] = start_time
                group_copy['end_day'] = end_day.strftime('%A')
                group_copy['end_time'] = end_time

                # Calculate time-based toll rates and add to result DataFrame
                group_copy['toll_rate'] = group_copy['distance'] * discount_factor
                result_df = pd.concat([result_df, group_copy])

    return result_df.reset_index(drop=True)


    return df


# reference_id = 1001402
# path_for_dataset3="D:\mapup_Assignment\MapUp-Data-Assessment-F\datasets\dataset-3.csv"
# ds_3=pd.read_csv(path_for_dataset3)
# # print(ds_3.shape)
# dist_mat=calculate_distance_matrix(ds_3)
# # print(dist_mat)
# unroll_dist_mat=unroll_distance_matrix(dist_mat)
# # print(unroll_dist_mat)
# ten_percent_id=find_ids_within_ten_percentage_threshold(unroll_dist_mat,reference_id)

# # print(ten_percent_id)

# rate_df=calculate_toll_rate(unroll_dist_mat)    
# # print(rate_df)

# time_toll_rate=calculate_time_based_toll_rates(ten_percent_id)
# print(time_toll_rate)