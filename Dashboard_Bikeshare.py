import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import jinja2 
import streamlit as st

sns.set(style='dark')

#Mendefinisikan function
def get_total_count_by_hour_df(df_hour):
  hour_count_df =  df_hour.groupby(by="hr").agg({
      "cnt": ["sum"]})
  return hour_count_df

def count_by_day_df(df_day):
    day_df_count_2011 = df_day.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return day_df_count_2011

def total_registered_df(df_day):
   reg_df =  df_day.groupby(by="dteday").agg({
      "registered": ["sum"]
    })
   reg_df = reg_df.reset_index()
   reg_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg_df

def total_casual_df(df_day):
   cas_df =  df_day.groupby(by="dteday").agg({
      "casual": ["sum"]
    })
   cas_df = cas_df.reset_index()
   cas_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas_df

def sum_order (df_hour):
    sum_order_items_df = df_hour.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def macem_season (df_day): 
    season_df = df_day.groupby(by="season").cnt.sum().reset_index() 
    return season_df

df_day = pd.read_csv("day.csv")
df_hour = pd.read_csv("hour.csv")

datetime_columns = ["dteday"]
df_day.sort_values(by="dteday", inplace=True)
df_day.reset_index(inplace=True)   

df_hour.sort_values(by="dteday", inplace=True)
df_hour.reset_index(inplace=True)

for column in datetime_columns:
    df_day[column] = pd.to_datetime(df_day[column])
    df_hour[column] = pd.to_datetime(df_hour[column])

min_date_days = df_day["dteday"].min()
max_date_days = df_day["dteday"].max()

min_date_hour = df_hour["dteday"].min()
max_date_hour = df_hour["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_days = df_day[(df_day["dteday"] >= str(start_date)) & 
                       (df_day["dteday"] <= str(end_date))]

main_df_hours = df_hour[(df_hour["dteday"] >= str(start_date)) & 
                        (df_hour["dteday"] <= str(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hours)
day_df_count_2011 = count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hours)
season_df = macem_season(main_df_hours)

#Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Bike Buddy : Rental Bike')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = day_df_count_2011.cnt.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)


#Visualisasi Data Bike Buddy Company Revenue in 2011-2012
st.subheader("Bike Buddy Company Revenue in 2011-2012")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    df_day["dteday"],
    df_day["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)


#Visualisasi Data Perbandingan Customer yang Registered dengan Casual
st.subheader("Comparison between Registered customers and Casual customers")

sizes = [18, 70]
explode = (0, 0.1) 

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=['Casual', 'Registered'], autopct='%1.1f%%',colors=["#F2A229", "#4034EB"],
        shadow=True, startangle=90)
ax1.axis('equal')  
st.pyplot(fig1) 


#Visualisasi Data Distribusi Customer Bike share pada tiap jam baik di hari kerja maupun hari libur
#WEEKDAY
st.subheader("Specific hours do bikes most in demand both on weekdays")
fig, ax = plt.subplots(figsize=(12,6))
sns.boxplot(x='hr', y='cnt', data=df_hour[df_hour['workingday']==1], ax=ax,color="#4034eb")
ax.grid(False)

for line in ax.lines:
    if line.get_marker() == 'o':  
        line.set_marker('o')
        line.set_markersize(3)

st.pyplot(fig)

#WEEKEND
st.subheader("Specific hours do bikes most in demand both on weekend")
fig, ax = plt.subplots(figsize=(12,6))
sns.boxplot(x='hr', y='cnt', data=df_hour[df_hour['workingday']==0], ax=ax,color="#4034eb")
ax.grid(False)

for line in ax.lines:
    if line.get_marker() == 'o':  
        line.set_marker('o')
        line.set_markersize(3)

st.pyplot(fig)

#Visualisasi Data Korelasi suhu dengan jumlah Customer Bike share
st.subheader('Correlation between Temperature and Customer')
df_day['temp'] = df_day['temp'] * 41
    
fig, ax = plt.subplots(figsize=(10, 4))
sns.histplot(x='temp', data=df_day, ax=ax,color="#F2A229")
ax.set_title('Distribution of Temperature')
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Frequency')

st.pyplot(fig)

#Menuliskan Kesimpulan yang menjawab 2 Pertanyaan Analisa 
st.subheader('Conclusion')
st.write(
""" Dapat disimpulkan bahwa pada Weekday fasilitas bikeshare banyak digunakan sebagai transportasi untuk berangkat-pulang kerja 
    atau ke sekolah dikarenakan peminatnya berada paling tinggi pada pukul 8 pagi, 5 sore, dan 6 sore. Sedangkan pada saat Weekend, 
    bikeshare cukup diminati untuk bepergian karena paling banyak digunakan pada jam aktif manusia yaitu mulai dari pukul 12 siang hingga 5 sore.
    Selain itu, suhu di luar ruangan cukup mempengaruhi penggunaan bikeshare. Hal ini dibuktikan melalui dataset "day" yang menunjukkan bahwa saat temperatur 
    berada diantara 10-30 degC, bikeshare banyak digunakan. Untuk suhu rendah (< 10degC) dan suhu tinggi (>30degC), bikeshare jarang diminati orang.
    """
)