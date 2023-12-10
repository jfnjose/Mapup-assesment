#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
df = pd.read_csv("F:\Submission\MapUp-Data-Assessment-F\datasets\dataset-3.csv")


# # Question 1

# In[ ]:


def calculate_distance_matrix(df):
    toll_ids = set(df['id_start'].unique()).union(df['id_end'].unique())
    distance_matrix = pd.DataFrame(index=toll_ids, columns=toll_ids).fillna(0)
    for index, row in df.iterrows():
        toll_a, toll_b, distance = row['id_start'], row['id_end'], row['distance']
        distance_matrix.at[toll_a, toll_b] += distance
        distance_matrix.at[toll_b, toll_a] += distance

    return distance_matrix
resulting_matrix = calculate_distance_matrix(df)
print(resulting_matrix)


# In[ ]:


def unroll_distance_matrix(distance_matrix):
    upper_triangle = distance_matrix.where(np.triu(np.ones(distance_matrix.shape), k=1).astype(bool))
    unrolled_df = upper_triangle.stack().reset_index()
    unrolled_df.columns = ['id_start', 'id_end', 'distance']

    return unrolled_df
unrolled_distance_df = unroll_distance_matrix(resulting_matrix)
print(unrolled_distance_df)


# In[ ]:


def find_ids_within_ten_percentage_threshold(distance_df, reference_value):
    subset_df = distance_df[distance_df['id_start'] == reference_value]
    reference_average_distance = subset_df['distance'].mean()
    threshold = 0.1 * reference_average_distance
    within_threshold_df = subset_df[
        (subset_df['distance'] >= reference_average_distance - threshold) &
        (subset_df['distance'] <= reference_average_distance + threshold)
    ]
    result_ids = sorted(within_threshold_df['id_start'].unique())

    return result_ids
reference_value = 1
result_ids_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_distance_df, reference_value)
print(result_ids_within_threshold)


# In[ ]:


def calculate_toll_rate(distance_df):
    result_df = distance_df.copy()
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        result_df[vehicle_type] = result_df['distance'] * rate_coefficient

    return result_df
result_with_toll_rates = calculate_toll_rate(unrolled_distance_df)
print(result_with_toll_rates)


# In[ ]:


from datetime import datetime, time, timedelta
def calculate_time_based_toll_rates(toll_rate_df):
    result_df = toll_rate_df.copy()
    weekday_time_ranges = [(time(0, 0, 0), time(10, 0, 0)),
                           (time(10, 0, 0), time(18, 0, 0)),
                           (time(18, 0, 0), time(23, 59, 59))]

    weekend_time_range = (time(0, 0, 0), time(23, 59, 59))
    weekday_discount_factors = [0.8, 1.2, 0.8]
    weekend_discount_factor = 0.7
    time_based_rates = []
    for index, row in result_df.iterrows():
        start_datetime = datetime.combine(datetime.today(), row['start_time'])
        end_datetime = datetime.combine(datetime.today(), row['end_time'])
        start_day = start_datetime.strftime('%A')
        end_day = end_datetime.strftime('%A')
        if start_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            for i, time_range in enumerate(weekday_time_ranges):
                if time_range[0] <= row['start_time'] <= time_range[1] and time_range[0] <= row['end_time'] <= time_range[1]:
                    discount_factor = weekday_discount_factors[i]
                    break
        else:
            discount_factor = weekend_discount_factor
        time_based_rate = row['distance'] * discount_factor
        time_based_rates.append((start_day, row['start_time'], end_day, row['end_time'], time_based_rate))
    time_based_df = pd.DataFrame(time_based_rates, columns=['start_day', 'start_time', 'end_day', 'end_time', 'time_based_rate'])
    result_df = pd.concat([result_df, time_based_df], axis=1)

    return result_df
result_with_time_based_rates = calculate_time_based_toll_rates(result_with_toll_rates)
print(result_with_time_based_rates)

