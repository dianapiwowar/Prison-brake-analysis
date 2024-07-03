#!/usr/bin/env python
# coding: utf-8

# Analyzing a dataset about the westbound traffic on the I-94 Interstate highway.

# In[1]:


import pandas as pd
traffic = pd.read_csv('Metro_Interstate_Traffic_Volume.csv')


# In[2]:


traffic.info()


# In[6]:


print(traffic.head(5))
print(traffic.tail(5))
print(traffic['weather_main'].unique())


# In[8]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[14]:


plt.hist(traffic['traffic_volume'])
plt.show()


# In[13]:


traffic['traffic_volume'].describe()


# Transforming date_time, and divide by day and night
# 

# In[20]:


traffic['date_time'] = pd.to_datetime(traffic['date_time'])


# In[21]:


print(type(traffic['date_time']))


# In[29]:


# Extract the hour from the 'date_time' column
traffic['hour'] = traffic['date_time'].dt.hour

# Define daytime and nighttime hours (assuming daytime is from 7 AM to 7 PM)
daytime_hours = range(7, 19)  # 7 AM to 7 PM
nighttime_hours = list(range(19, 24)) + list(range(0, 7))  # 7 PM to 7 AM

# Isolate daytime data
daytime_data = traffic[traffic['hour'].isin(daytime_hours)]

# Isolate nighttime data
nighttime_data = traffic[traffic['hour'].isin(nighttime_hours)]

# Print the isolated data
print("Daytime Data:")
print(daytime_data)
print("\nNighttime Data:")
print(nighttime_data)


# In[23]:





# Plot the histograms of traffic_volume for both day and night. Organize the two histograms side-by-side on a grid chart.

# In[36]:


# Nighttime traffic volume
plt.subplot(1, 2, 1)
plt.hist(nighttime_data['hour'], edgecolor='black')
plt.title("Nighttime Traffic Volume")
plt.xlabel('Hour of the Day')
plt.ylabel('Frequency')
plt.xlim([0, 24])

# Daytime traffic volume
plt.subplot(1, 2, 2)
plt.hist(daytime_data['hour'],  edgecolor='black')
plt.title("Daytime Traffic Volume")
plt.xlabel('Hour of the Day')
plt.ylabel('Frequency')
plt.xlim([0, 24])

plt.tight_layout()
plt.show()


# Group by month

# In[50]:


traffic['month'] = traffic['date_time'].dt.month
by_month = traffic.groupby('month').mean()
print(by_month['traffic_volume'])
print(traffic.head(5))

print(type(by_month))

plt.plot(by_month['traffic_volume'])
plt.title('Traffic Volume AVG by Month')
plt.xlabel('Month')
plt.ylabel('Traffic Volume (Average)')
plt.xticks(range(1, 13))
plt.show()


# Group by day

# In[53]:


traffic['dayofweek'] = traffic['date_time'].dt.dayofweek
by_dayofweek = traffic.groupby('dayofweek').mean()
by_dayofweek['traffic_volume']  # 0 is Monday, 6 is Sunday

plt.plot(by_dayofweek['traffic_volume'])
plt.title('Traffic Volume AVG by DOW')
plt.xlabel('Day')
plt.ylabel('Traffic Volume (Average)')
plt.xticks(range(1, 7))
plt.show()


# In[55]:


traffic['hour'] = traffic['date_time'].dt.hour
bussiness_days = traffic.copy()[traffic['dayofweek'] <= 4] # 4 == Friday
weekend = traffic.copy()[traffic['dayofweek'] >= 5] # 5 == Saturday
by_hour_business = bussiness_days.groupby('hour').mean()
by_hour_weekend = weekend.groupby('hour').mean()

print(by_hour_business['traffic_volume'])
print(by_hour_weekend['traffic_volume'])


# Plot grid chart for businnes days and other 

# In[68]:


plt.figure(figsize=(10, 6))

# Business days traffic volume
plt.subplot(1, 2, 1)
plt.plot(by_hour_business['traffic_volume'], linewidth=0.5)
plt.title("Business Days Traffic Volume")
plt.xlabel('Hour of the Day')
plt.ylabel('Frequency')
plt.xticks(range(0, 24, 2))  # Show ticks every 2 units on the x-axis
plt.xlim([0, 24])
plt.grid(True)

# Other days traffic volume
plt.subplot(1, 2, 2)
plt.plot(by_hour_weekend['traffic_volume'], linewidth=0.5)
plt.title("Weekend Traffic Volume")
plt.xlabel('Hour of the Day')
plt.ylabel('Frequency')
plt.xticks(range(0, 24, 2))  # Show ticks every 2 units on the x-axis
plt.xlim([0, 24])

plt.grid(True)
plt.show()


# Conclusions:
# 1. On business days we have the highest avg traffic betwen 8 and 10 am and then about 4 pm. This is propably connectwed with working hours.
# 
# 2. On the weekend avg traffic increase from 4 am, but the highest is between 12 and 4 pm. On weekends we are sleeping longer, and we go to a shop or for a trip a bit later.

# In[74]:


# Calculate correlation of traffic_volume with all other numeric columns
correlation_matrix = traffic.corr()['traffic_volume']
print(correlation_matrix)


# In[79]:


##The highest correlation from weather incicators is with temp: 
#Print scatter plot with traffic_volume and temp column

plt.figure(figsize=(8, 6))
plt.scatter(traffic['traffic_volume'], traffic['temp'], color='blue', alpha=0.5)
plt.title('Scatter Plot of Traffic Volume vs Temperature')
plt.xlabel('Traffic Volume')
plt.ylabel('Temperature')
plt.grid(True)
plt.show()


# There are no any reliable conslusion from this plot

# In[86]:


## Calculate the average traffic volume associated with each unique value 
## in weather_main and weather_description


by_weather_main = traffic.groupby('weather_main').mean()
by_weather_description = traffic.groupby('weather_description').mean()
print(by_weather_main)


# In[91]:


# Plot a horizontal bar plot for the traffic_volume column of by_weather_main
plt.figure(figsize=(10, 6))
plt.barh(by_weather_main.index, by_weather_main['traffic_volume'], color='skyblue')
plt.xlabel('Average Traffic Volume')
plt.ylabel('Weather Main')
plt.title('Average Traffic Volume by Weather Main')
plt.grid(True)
plt.show()


# In[97]:


# Plot a horizontal bar plot for the traffic_volume column of by_weather_description
plt.figure(figsize=(5, 10))
plt.barh(by_weather_description.index, by_weather_description['traffic_volume'], color='skyblue')
plt.xlabel('Average Traffic Volume')
plt.ylabel('Weather Main')
plt.title('Average Traffic Volume by weather description')
plt.grid(True)
plt.show()


# Impact of Weather on Traffic Volume:
# 
#     Clear weather has the highest average traffic volume, indicating that generally, clearer weather conditions might encourage more people to travel.
#     Clouds and Rain follow with relatively high average traffic volumes, suggesting that these weather conditions still permit substantial travel.
#     Snow and Fog have lower average traffic volumes, likely due to the more challenging driving conditions they present.
# 
# Traffic Behavior During Extreme Conditions:
# 
#     Thunderstorm and Squall conditions show significantly lower average traffic volumes. This indicates that people tend to avoid travel during severe weather events, prioritizing safety.
# 
# Influence of Weather Variables:
# 
#     Temperature (temp) might play a role in traffic volume, although the correlation and impact weren't explicitly shown in the provided analysis.
#     Rainfall (rain_1h) and Snowfall (snow_1h), while included in the dataset, didn't show a direct correlation with traffic volume in the provided analysis but could be explored further.
# 
# Visualization Insights:
# 
#     The horizontal bar plot effectively showcases the varying average traffic volumes across different weather conditions.
#     Clear labels and titles help interpret the data easily, making it clear which weather conditions correlate with higher or lower traffic volumes.

# In[ ]:




