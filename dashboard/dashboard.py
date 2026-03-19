import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# 1. Helper Functions
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
    return rfm_df

# 2. Load Data
all_df = pd.read_csv("all_data.csv")

# Memastikan kolom tanggal bertipe datetime
datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
for column in datetime_columns:
    if column in all_df.columns:
        all_df[column] = pd.to_datetime(all_df[column])

# Mengurutkan data berdasarkan tanggal pembelian
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(drop=True, inplace=True)

# 3. Filter Komponen (Sidebar)
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    # Menambahkan logo perusahaan (bisa diganti URL gambar lain)
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Menyaring data utama berdasarkan input tanggal di sidebar
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

# Memanggil helper functions dengan data yang sudah disaring
daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
rfm_df = create_rfm_df(main_df)

# 4. Melengkapi Dashboard Utama
st.header('E-Commerce Public Dashboard :sparkles:')

# --- A. Daily Orders & Revenue ---
st.subheader('Daily Orders')

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

# --- B. Best & Worst Performing Products ---
st.subheader("Best & Worst Performing Products")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 10))
colors = ["#72BCD4"] * 5 + ["#D3D3D3"] * 5

# Best Product
sns.barplot(x="order_item_id", y="product_category_name_english", data=sum_order_items_df.head(10), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=15)
ax[0].set_title("Best Performing Product", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

# Worst Product
sns.barplot(x="order_item_id", y="product_category_name_english", data=sum_order_items_df.sort_values(by="order_item_id", ascending=True).head(10), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=15)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

st.pyplot(fig)

# --- C. RFM Analysis ---
st.subheader("Best Customer Based on RFM Parameters")

col1, col2, col3 = st.columns(3)
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), "BRL", locale='pt_BR')
    st.metric("Average Monetary", value=avg_frequency)

fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(15, 20))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Mengambil top 5 dan membuat short ID
rfm_recency = rfm_df.sort_values(by="recency", ascending=True).head(5).copy()
rfm_recency['short_id'] = rfm_recency['customer_unique_id'].str[:8]
sns.barplot(y="recency", x="short_id", data=rfm_recency, palette=colors, ax=ax[0])
ax[0].set_ylabel("Days", fontsize=15)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (Days)", loc="center", fontsize=20)
ax[0].tick_params(axis='x', labelsize=15)

rfm_frequency = rfm_df.sort_values(by="frequency", ascending=False).head(5).copy()
rfm_frequency['short_id'] = rfm_frequency['customer_unique_id'].str[:8]
sns.barplot(y="frequency", x="short_id", data=rfm_frequency, palette=colors, ax=ax[1])
ax[1].set_ylabel("Frequency", fontsize=15)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=20)
ax[1].tick_params(axis='x', labelsize=15)

rfm_monetary = rfm_df.sort_values(by="monetary", ascending=False).head(5).copy()
rfm_monetary['short_id'] = rfm_monetary['customer_unique_id'].str[:8]
sns.barplot(y="monetary", x="short_id", data=rfm_monetary, palette=colors, ax=ax[2])
ax[2].set_ylabel("Monetary", fontsize=15)
ax[2].set_xlabel("Customer ID", fontsize=15)
ax[2].set_title("By Monetary", loc="center", fontsize=20)
ax[2].tick_params(axis='x', labelsize=15)

plt.tight_layout(pad=3.0)
st.pyplot(fig)

st.caption('Copyright (c) Dini Arya Putri 2024')