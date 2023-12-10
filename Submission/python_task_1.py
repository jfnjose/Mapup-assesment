#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
dataframe = pd.read_csv("F:\Submission\MapUp-Data-Assessment-F\datasets\dataset-1.csv")


# # Question 2

# In[ ]:


def get_type_count(dataframe):
    dataframe['car_type'] = pd.cut(dataframe['car'],
                                   bins=[-float('inf'), 15, 25, float('inf')],
                                   labels=['low', 'medium', 'high'],
                                   right=False)   
    type_counts = dataframe['car_type'].value_counts().to_dict()
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts
result = get_type_count(dataframe)
print(result)


# # Question 3

# In[ ]:


def get_bus_indexes(dataframe):
    mean_bus_value = dataframe['bus'].mean()
    bus_indexes = dataframe[dataframe['bus'] > 2 * mean_bus_value].index.tolist()
    bus_indexes.sort()
    return bus_indexes

result = get_bus_indexes(dataframe)
print(result)


# # Question 4

# In[ ]:


def filter_routes(dataframe):
    route_avg_truck = dataframe.groupby('route')['truck'].mean()
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    selected_routes.sort()
    return selected_routes
result = filter_routes(dataframe)
print(result)


# # Question 6

# In[3]:


dataframe_2= pd.read_csv("F:\Submission\MapUp-Data-Assessment-F\datasets\dataset-2.csv")


# In[ ]:


def verify_timestamps(dataframe_2):
    dataframe_2['start_timestamp'] = pd.to_datetime(dataframe_2['startDay'] + ' ' + dataframe_2['startTime'])
    dataframe_2['end_timestamp'] = pd.to_datetime(dataframe_2['endDay'] + ' ' + dataframe_2['endTime'])
    mask = (
        (dataframe_2['start_timestamp'].dt.time != pd.Timestamp('00:00:00').time()) |
        (dataframe_2['end_timestamp'].dt.time != pd.Timestamp('23:59:59').time()) |
        ~dataframe_2['start_timestamp'].dt.dayofweek.between(0, 6) |
        ~dataframe_2['end_timestamp'].dt.dayofweek.between(0, 6) |
        (dataframe_2['end_timestamp'] - dataframe_2['start_timestamp'] != pd.to_timedelta('1 day'))
    )
    result = mask.groupby(['id', 'id_2']).any()
    return result

result = verify_timestamps(dataframe_2)
print(result)


# In[ ]:




