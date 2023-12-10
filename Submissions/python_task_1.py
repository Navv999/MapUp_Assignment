import pandas as pd
import numpy as np


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    df=df.pivot(index='id_1', columns='id_2', values='car')
    for idx in df.index:
        df.at[idx, idx] = 0
    

    return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    conditions = [
        (df['car'] <= 15),
        ((df['car'] > 15) & (df['car'] <= 25)),
        (df['car'] > 25)
    ]
    choices = ['low', 'medium', 'high']

    # Create 'car_type' column based on conditions
    df['car_type'] = pd.Categorical(np.select(conditions, choices, default='Unknown'))

    # Calculate count of occurrences for each 'car_type' category
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    type_counts = dict(sorted(type_counts.items()))

   

    return type_counts


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    bus_mean = df['bus'].mean()
    
    # Identify indices where 'bus' values are greater than twice the mean
    bus_indices = df[df['bus'] > 2 * bus_mean].index.tolist()
    
    # Sort the indices in ascending order
    bus_indices.sort()

    return bus_indices


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    average_truck_by_route = df.groupby('route')['truck'].mean()

    # Filter routes where the average 'truck' value is greater than 7
    selected_routes = average_truck_by_route[average_truck_by_route > 7].index.tolist()

    # Sort the list of selected routes
    selected_routes.sort()

    return selected_routes

    # return list()


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    modified_matrix = matrix.copy()

    # Apply the specified logic to modify values
    modified_matrix = modified_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df['timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])

    # Extract day of the week and hour from the timestamp
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['hour'] = df['timestamp'].dt.hour

    # Check if each (id, id_2) pair covers a full 24-hour period and spans all 7 days
    completeness_check = (
        (df.groupby(['id', 'id_2'])['hour'].nunique() == 24) &
        (df.groupby(['id', 'id_2'])['day_of_week'].nunique() == 7)
    )

    return completeness_check

# path_for_dataset_1="D:\mapup_Assignment\MapUp-Data-Assessment-F\datasets\dataset-1.csv"
# path_for_dataset_2="D:\mapup_Assignment\MapUp-Data-Assessment-F\datasets\dataset-2.csv"
# df_1=pd.read_csv(path_for_dataset_1)
# df_2=pd.read_csv(path_for_dataset_2)
# print(df_2.head(20))
# res_mat=generate_car_matrix(df_1)
# # print(df2.head(5))
# # print(df_1.head(20))
# dict1={}
# dict1=get_type_count(df_1)
# # print(dict1)
# # print(df_1.head(20))
# l1=[]
# l1=get_bus_indexes(df_1)
# # print(l1)
# l2=[]
# l2=get_bus_indexes(df_1)
# # print(l2)
# res_mat=multiply_matrix(res_mat)
# print(res_mat)
# l3=[]
# l3=time_check(df_2)
# print(l3)
