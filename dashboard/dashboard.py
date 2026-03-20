import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import streamlit as st
from babel.numbers import format_currency

sns.set_theme(style="whitegrid")
st.set_page_config(page_title="E-Commerce Dashboard")

# --- Helper Functions ---
def create_daily_orders_df(df):
    return df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "price": "sum"
    }).reset_index().rename(columns={"order_id": "order_count", "price": "revenue"})

def create_sum_order_items_df(df):
    return df.groupby("product_category_name_english").order_item_id.sum().sort_values(ascending=False).reset_index()

def create_bystate_df(df):
    return df.groupby("customer_state").customer_id.nunique().sort_values(ascending=False).reset_index().rename(columns={"customer_id": "customer_count"})

def create_rfm_df(df):
    rfm_df = df.groupby("customer_unique_id").agg({
        "order_purchase_timestamp": "max",
        "order_id": "nunique",
        "price": "sum"
    }).reset_index()

    rfm_df.columns = ["customer_unique_id", "max_date", "frequency", "monetary"]
    recent_date = df["order_purchase_timestamp"].max()
    rfm_df["recency"] = (recent_date - rfm_df["max_date"]).dt.days

    # Segmentation
    def segment(row):
        if row['recency'] <= 30 and row['frequency'] > 1:
            return 'Loyal'
        elif row['recency'] <= 60:
            return 'Recent'
        elif row['recency'] > 180:
            return 'At Risk'
        else:
            return 'Standard'

    rfm_df["segment"] = rfm_df.apply(segment, axis=1)
    return rfm_df

# --- Load Data ---
# Mendapatkan path folder tempat dashboard.py ini berada
directory = os.path.dirname(__file__)
path = os.path.join(directory, "all_data.csv")

# Baca file menggunakan path yang sudah digabung
all_df = pd.read_csv(path)

all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"])
all_df.sort_values("order_purchase_timestamp", inplace=True)

# --- Sidebar ---
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    start_date, end_date = st.date_input("Rentang Waktu", [min_date, max_date])

    state_filter = st.multiselect(
        "Filter State",
        options=all_df["customer_state"].unique(),
        default=all_df["customer_state"].unique()
    )

# --- Filter Data ---
main_df = all_df[
    (all_df["order_purchase_timestamp"] >= str(start_date)) &
    (all_df["order_purchase_timestamp"] <= str(end_date)) &
    (all_df["customer_state"].isin(state_filter))
]

daily_orders_df = create_daily_orders_df(main_df)
product_df = create_sum_order_items_df(main_df)
bystate_df = create_bystate_df(main_df)
rfm_df = create_rfm_df(main_df)

# --- Dashboard ---
st.title("📊 E-Commerce Dashboard")

# KPI
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", daily_orders_df.order_count.sum())
col2.metric("Revenue", format_currency(daily_orders_df.revenue.sum(), "BRL", locale='pt_BR'))
col3.metric("Avg Order Value", round(main_df["price"].mean(), 2))

# --- Trend ---
st.subheader("Trend Orders")
fig, ax = plt.subplots()
ax.plot(daily_orders_df["order_purchase_timestamp"], daily_orders_df["order_count"])
st.pyplot(fig)

st.markdown("Insight: Terdapat pola fluktuasi dengan kenaikan pada periode tertentu (seasonality).")

# --- Products ---
st.subheader("Top Products")
fig, ax = plt.subplots()
sns.barplot(x="order_item_id", y="product_category_name_english", data=product_df.head(10), ax=ax)
st.pyplot(fig)

st.markdown("Insight: Beberapa kategori mendominasi penjualan.")

# --- State ---
st.subheader("Customer Distribution by State")
fig, ax = plt.subplots()
sns.barplot(x="customer_count", y="customer_state", data=bystate_df.head(10), ax=ax)
st.pyplot(fig)

st.markdown("Insight: Pelanggan terkonsentrasi di beberapa wilayah utama.")

# --- MAP ---
st.subheader("Geospatial Map")
if "geolocation_lat" in all_df.columns:
    geo = all_df[['geolocation_lat', 'geolocation_lng']].dropna()
    geo = geo.rename(columns={'geolocation_lat': 'lat', 'geolocation_lng': 'lon'})
    st.map(geo.sample(1000))

# --- RFM ---
st.subheader("RFM Analysis")

col1, col2, col3 = st.columns(3)
col1.metric("Avg Recency", round(rfm_df.recency.mean(), 1))
col2.metric("Avg Frequency", round(rfm_df.frequency.mean(), 2))
col3.metric("Avg Monetary", round(rfm_df.monetary.mean(), 2))

# Scatter
fig, ax = plt.subplots()
sns.scatterplot(x="recency", y="monetary", size="frequency", data=rfm_df, ax=ax)
st.pyplot(fig)

st.markdown("Insight: Pelanggan aktif (recency rendah) memiliki kontribusi revenue tinggi.")

# Segment
segment_counts = rfm_df["segment"].value_counts().reset_index()
segment_counts.columns = ["Segment", "Count"]

fig, ax = plt.subplots()
sns.barplot(x="Count", y="Segment", data=segment_counts, ax=ax)
st.pyplot(fig)

# Download
st.download_button("Download Data", main_df.to_csv(index=False), "data.csv")

st.caption("© Dini Arya Putri")
