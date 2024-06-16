import pandas as pd
import streamlit as st

# Load cleaned data
df = pd.read_csv('cleaned_hour.csv')
df['dteday'] = pd.to_datetime(df['dteday'])

def create_monthly_users_df(df):
    monthly_users_df = df.resample(rule='M', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    monthly_users_df.index = monthly_users_df.index.strftime('%b-%y')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "dteday": "dateyears",
        "casual": "casual_users",
        "registered": "registered_users",
        "cnt": "total_users"
    }, inplace=True)
    
    return monthly_users_df

def create_seasonly_users_df(df):
    seasonly_users_df = df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    seasonly_users_df = seasonly_users_df.reset_index()
    seasonly_users_df.rename(columns={
        "casual": "casual_users",
        "registered": "registered_users",
        "cnt": "total_users"
    }, inplace=True)

    seasonly_users_df['season'] = pd.Categorical(seasonly_users_df['season'],
                                             categories=['Spring', 'Summer', 'Fall', 'Winter'])
    
    seasonly_users_df = seasonly_users_df.sort_values('season')
    
    return seasonly_users_df

def create_weekday_users_df(df):
    weekday_users_df = df.groupby("weekday").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    weekday_users_df = weekday_users_df.reset_index()
    weekday_users_df.rename(columns={
        "casual": "casual_users",
        "registered": "registered_users",
        "cnt": "total_users"
    }, inplace=True)
    
    weekday_users_df['weekday'] = pd.Categorical(weekday_users_df['weekday'],
                                             categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    weekday_users_df = weekday_users_df.sort_values('weekday')
    
    return weekday_users_df

def create_hourly_users_df(df):
    hourly_users_df = df.groupby("hr").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    hourly_users_df = hourly_users_df.reset_index()
    hourly_users_df.rename(columns={
        "casual": "casual_users",
        "registered": "registered_users",
        "cnt": "total_users"
    }, inplace=True)
    
    return hourly_users_df

def create_weatherly_users_df(df):
    weatherly_users_df = df.groupby("weathersit").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    weatherly_users_df = weatherly_users_df.reset_index()
    weatherly_users_df.rename(columns={
        "casual": "casual_users",
        "registered": "registered_users",
        "cnt": "total_users"
    }, inplace=True)
    
    return weatherly_users_df

# Filter data
min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df["dteday"] >= str(start_date)) & 
                (df["dteday"] <= str(end_date))]

monthly_users_df = create_monthly_users_df(main_df)
weekday_users_df = create_weekday_users_df(main_df)
seasonly_users_df = create_seasonly_users_df(main_df)
hourly_users_df = create_hourly_users_df(main_df)
weatherly_users_df = create_weatherly_users_df(main_df)

st.title('Bike-sharing Dashboard :sparkles:')
st.sidebar.markdown(
    """
    #### Created By Endritha Pramudya 
"""
)
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/endritha/)")
st.sidebar.markdown("[Github](https://github.com/NVREND)")

st.markdown("##")
col1, col2, col3 = st.columns(3)
with col1:
    total_registered_users = main_df['registered'].sum()
    st.metric("Total Registered User", value=total_registered_users)
with col2:
    total_casual_users = main_df['casual'].sum()
    st.metric("Total Casual User", value=total_casual_users)
with col3:
    total_all_users = main_df['cnt'].sum()
    st.metric("Total User", value=total_all_users)
st.markdown("---")

st.subheader("Monthly Count of Bikeshare Users")
st.line_chart(data=monthly_users_df.set_index('dateyears')[['total_users']])
st.line_chart(data=monthly_users_df.set_index('dateyears')[['casual_users', 'registered_users']])
st.markdown("---")

st.subheader("Count Bikeshare Users by Season")
st.bar_chart(data=seasonly_users_df.set_index('season')[['total_users']])
st.bar_chart(data=seasonly_users_df.set_index('season')[['casual_users', 'registered_users']])
st.markdown("---")

st.subheader("Count Bikeshare Users by Weather")
st.bar_chart(data=weatherly_users_df.set_index('weathersit')[['total_users']])
st.bar_chart(data=weatherly_users_df.set_index('weathersit')[['casual_users', 'registered_users']])

st.markdown(
    """
    ###### weathersit : 
    1: Clear, Few clouds, Partly cloudy, Partly cloudy
    2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
    3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
    4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
"""
)

st.caption('Copyright (c), created by Endritha Pramudya')
