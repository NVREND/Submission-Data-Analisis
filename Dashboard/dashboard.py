import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

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
                                             categories=['Springer', 'Summer', 'Fall', 'Winter'])
    
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
    # Menambahkan logo perusahaan
    st.image("bicycle.jpg")
    
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
weekday_users_df = create_weatherly_users_df(main_df)

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
fig, ax = plt.subplots(figsize=(35, 15))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.lineplot(x="dateyears", y="total_users", data=monthly_users_df, marker='o', linewidth=4, palette=colors, ax=ax)
ax.set_ylabel(None)
ax.set_xlabel("Date", fontsize=30)
ax.set_title("Monthly Count of Bikeshare Users", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=25)
plt.tight_layout()
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(35, 15))
colors = ["#72BCD4", "#FFA500"]
monthly_users_df_melted = monthly_users_df.melt(id_vars=['dateyears'], value_vars=['casual_users', 'registered_users'])

sns.lineplot(x='dateyears', y='value', hue='variable', data=monthly_users_df_melted, marker='o', linewidth=4,palette=colors, ax=ax)
ax.legend(fontsize=20)
ax.set_ylabel("Number of Orders", fontsize=30)
ax.set_xlabel("Date", fontsize=30)
ax.set_title("Monthly Count of Bikeshare Users", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=25)
ax.tick_params(axis='x', labelsize=25)
st.pyplot(fig)

st.markdown("---")

st.subheader("Count Bikeshare Users by Season")
fig, ax = plt.subplots(figsize=(35, 15))
colors = ["#72BCD4"]

sns.barplot(x="season", y="total_users", data=seasonly_users_df, palette=colors, ax=ax)
ax.set_ylabel("Total Users", fontsize=30)
ax.set_xlabel("Season", fontsize=30)
ax.set_title("Count Bikeshare Users by Season", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=25)
st.pyplot(fig)


fig, ax = plt.subplots(figsize=(35, 15))
colors = ["#72BCD4", "#FFA500"]
seasonly_users_df_melt = pd.melt(seasonly_users_df,
                                id_vars=['season'],
                                value_vars=['casual_users', 'registered_users'],
                                var_name='status',
                                value_name='count_users')

sns.barplot(x='season', y='count_users', data=seasonly_users_df_melt, hue='status')
ax.legend(fontsize=20)
ax.set_ylabel("Total Users", fontsize=30)
ax.set_xlabel("Season", fontsize=30)
ax.set_title("Count of Bikeshare Users by Season", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=25)
ax.tick_params(axis='x', labelsize=25)
st.pyplot(fig)

st.markdown("---")

st.subheader("Count Bikeshare Users by Weather")
fig, ax = plt.subplots(figsize=(35, 15))
colors = ["#72BCD4"]

sns.barplot(x="weathersit", y="total_users", data=weekday_users_df, palette=colors, ax=ax)
ax.set_ylabel("Total Users", fontsize=30)
ax.set_xlabel("Weather", fontsize=30)
ax.set_title("Count Bikeshare Users by Weather", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=25)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(35, 15))
colors = ["#72BCD4", "#FFA500"]
weatherly_users_df_melt = pd.melt(weekday_users_df,
                                id_vars=['weathersit'],
                                value_vars=['casual_users', 'registered_users'],
                                var_name='status',
                                value_name='count_users')
sns.barplot(x='weathersit', y='count_users', data=weatherly_users_df_melt, hue='status')
ax.legend(fontsize=20)
ax.set_ylabel("Total Users", fontsize=30)
ax.set_xlabel("Weather", fontsize=30)
ax.set_title("Count of Bikeshare Users by Weather", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=25)
ax.tick_params(axis='x', labelsize=25)
st.pyplot(fig)

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