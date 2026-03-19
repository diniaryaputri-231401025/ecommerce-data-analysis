import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# --- 1. Helper Functions ---
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "price": "sum"
    }).reset_index()
    daily_orders_df.rename(columns={"order_id": "order_count", "price": "revenue"}, inplace=True)
    return daily_orders_df

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_category_name_english").order_item_id.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_bystate_df(df):
    bystate_df = df.groupby(by="customer_state").customer_id.nunique().sort_values(ascending=False).reset_index()
    bystate_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
    return bystate_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_unique_id", as_index=False).agg({
        "order_purchase_timestamp": "max",
        "order_id": "nunique",
        "price": "sum"
    })
    rfm_df.columns = ["customer_unique_id", "max_order_timestamp", "frequency", "monetary"]
    
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["order_purchase_timestamp"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    
    # Teknik Analisis Lanjutan: Manual Clustering / Segmentation
    def segment_customer(row):
        if row['recency'] <= 30 and row['frequency'] > 1:
            return 'Loyal Customer'
        elif row['recency'] <= 60:
            return 'Recent Customer'
        elif row['recency'] > 180:
            return 'At Risk'
        else:
            return 'Standard'
            
    rfm_df['customer_segment'] = rfm_df.apply(segment_customer, axis=1)
    return rfm_df

# --- 2. Load Data ---
all_df = pd.read_csv("dashboard/all_data.csv")

datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
for column in datetime_columns:
    if column in all_df.columns:
        all_df[column] = pd.to_datetime(all_df[column])

all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(drop=True, inplace=True)

# --- 3. Filter Komponen (Sidebar) ---
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
bystate_df = create_bystate_df(main_df)
rfm_df = create_rfm_df(main_df)

# --- 4. Melengkapi Dashboard Utama ---
st.header('E-Commerce Public Dashboard :sparkles:')

# A. Daily Orders & Revenue
st.subheader('Daily Orders & Total Revenue')
col1, col2 = st.columns(2)
with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total Orders", value=total_orders)
with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "BRL", locale='pt_BR')
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(daily_orders_df["order_purchase_timestamp"], daily_orders_df["order_count"], marker='o', linewidth=2, color="#72BCD4")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# B. Best & Worst Performing Products
st.subheader("Best & Worst Performing Products")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 10))
colors = ["#72BCD4"] * 5 + ["#D3D3D3"] * 5

sns.barplot(x="order_item_id", y="product_category_name_english", data=sum_order_items_df.head(10), palette=colors, ax=ax[0], hue="product_category_name_english", legend=False)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=15)
ax[0].set_title("Best Performing Product", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

sns.barplot(x="order_item_id", y="product_category_name_english", data=sum_order_items_df.sort_values(by="order_item_id", ascending=True).head(10), palette=colors, ax=ax[1], hue="product_category_name_english", legend=False)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=15)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# C. Customer Demographics (Geospatial Proxy)
st.subheader("Customer Demographics by State")
fig, ax = plt.subplots(figsize=(12, 6))
colors_state = ["#72BCD4"] + ["#D3D3D3"] * 9
sns.barplot(x="customer_count", y="customer_state", data=bystate_df.head(10), palette=colors_state, ax=ax, hue="customer_state", legend=False)
ax.set_title("Top 10 States by Number of Customers", fontsize=15)
ax.set_xlabel("Customer Count")
ax.set_ylabel("State")
sns.despine()
st.pyplot(fig)

# D. RFM Analysis & Clustering
st.subheader("Customer Segmentation & RFM Analysis")
col1, col2, col3 = st.columns(3)
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
with col3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), "BRL", locale='pt_BR')
    st.metric("Average Monetary", value=avg_monetary)

# Menampilkan Distribusi Cluster Pelanggan
st.markdown("#### Customer Segmentation Distribution")
segment_counts = rfm_df['customer_segment'].value_counts().reset_index()
segment_counts.columns = ['Segment', 'Count']

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="Count", y="Segment", data=segment_counts.sort_values(by="Count", ascending=False), palette="viridis", ax=ax, hue="Segment", legend=False)
ax.set_xlabel("Number of Customers")
ax.set_ylabel(None)
sns.despine()
st.pyplot(fig)

st.caption('Copyright (c) Dini Arya Putri 2024')