# 🛒 E-Commerce Public Data Analysis Dashboard

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org/)

Proyek ini merupakan submission akhir untuk kelas **Belajar Analisis Data dengan Python** dari Dicoding. Proyek ini berfokus pada analisis *E-Commerce Public Dataset* dari Brazil untuk menghasilkan *business insight* berbasis data serta membangun *interactive dashboard* menggunakan Streamlit.

---

## 👤 Profil
- **Nama:** Dini Arya Putri  
- **Email:** diniarya135@gmail.com  
- **ID Dicoding:** CDCC319D6X1000  

---

## 🎯 Tujuan Proyek

Proyek ini bertujuan untuk:
- Melakukan proses analisis data end-to-end (data wrangling → EDA → visualization → insight)
- Menghasilkan insight bisnis yang actionable
- Mengimplementasikan teknik analisis lanjutan tanpa Machine Learning
- Menyajikan hasil analisis dalam bentuk dashboard interaktif

---

## ❓ Pertanyaan Bisnis

Analisis ini dirancang untuk menjawab pertanyaan berikut:

1. Bagaimana performa penjualan dan revenue perusahaan dalam beberapa bulan terakhir?
2. Produk apa yang memiliki performa terbaik dan terburuk berdasarkan jumlah penjualan?
3. Bagaimana distribusi pelanggan berdasarkan wilayah (state)?
4. Bagaimana segmentasi pelanggan berdasarkan perilaku transaksi menggunakan analisis RFM?
5. Bagaimana hubungan antara frekuensi transaksi dan total pengeluaran pelanggan?

---

## 📊 Teknik Analisis yang Digunakan

### 1. 📈 Exploratory Data Analysis (EDA)
- Analisis tren waktu (time series)
- Distribusi data
- Aggregation (groupby)

---

### 2. 🧠 RFM Analysis (Recency, Frequency, Monetary)
Digunakan untuk memahami perilaku pelanggan:

- **Recency:** Hari sejak transaksi terakhir
- **Frequency:** Jumlah transaksi
- **Monetary:** Total pengeluaran

➡️ Digunakan untuk mengidentifikasi:
- pelanggan aktif
- pelanggan loyal
- pelanggan berisiko churn

---

### 3. 🧩 Customer Segmentation (Manual Clustering)
Segmentasi pelanggan berdasarkan aturan bisnis:

- **Loyal Customer**
- **Recent Customer**
- **Standard**
- **At Risk**

➡️ Membantu strategi:
- retensi pelanggan
- targeting marketing

---

### 4. 🌍 Geospatial Analysis
Analisis distribusi pelanggan berdasarkan lokasi:

- Identifikasi wilayah dengan demand tinggi
- Analisis kepadatan pelanggan
- Insight untuk optimasi logistik & ekspansi pasar

---

### 5. 🔗 Correlation Analysis
Menganalisis hubungan antara:
- Frequency vs Monetary

➡️ Insight:
- pelanggan dengan frekuensi tinggi cenderung memiliki kontribusi revenue lebih besar

---

## 📁 Struktur Direktori

```text
ecommerce-data-analysis/
│
├── dashboard/
│   ├── dashboard.py       # Streamlit dashboard
│   └── all_data.csv       # Clean dataset
│
├── data/                  # Raw dataset
│
├── Proyek_Analisis_Data_Dini_Arya_Putri.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

### 🚀 Fitur Dashboard
Dashboard interaktif memiliki fitur:
- 📅 Filter rentang waktu
- 🌍 Filter berdasarkan state
- 📊 KPI (Total Orders, Revenue, Avg Order Value)
- 📈 Trend penjualan
- 🛍️ Analisis produk terlaris & terendah
- 📍 Distribusi pelanggan (state & map)
- 🧠 RFM Analysis (scatter plot + segmentation)

📥 Download dataset
### 🚀 Cara Menjalankan Dashboard Secara Lokal

1. Clone repository ini ke mesin lokal Anda:
   ```bash
   git clone [https://github.com/diniaryaputri-231401025/ecommerce-data-analysis.git](https://github.com/diniaryaputri-231401025/ecommerce-data-analysis.git)

2. Masuk ke direktori proyek:
   '''  Bash
   cd ecommerce-data-analysis

3. Instal library yang dibutuhkan (sangat disarankan menggunakan virtual environment):
   '''Bash
   pip install -r requirements.txt

4. Jalankan aplikasi Streamlit:
   '''Bash
   streamlit run dashboard/dashboard.py

## 🌐 Tautan Dashboard

Dashboard interaktif telah berhasil di-deploy ke Streamlit Community Cloud.  
Silakan akses melalui tautan berikut:

👉 [Buka E-Commerce Dashboard Disini](https://ecommerce-data-analysis-4kzv8bjmvfs7vcxdgqhrzo.streamlit.app/)

### 📌 Insight Utama
- Revenue menunjukkan pola musiman dengan puncak di akhir tahun
- Beberapa kategori produk mendominasi penjualan
- Pelanggan terkonsentrasi di wilayah tertentu (SP sebagai pusat utama)
- Sebagian besar pelanggan memiliki frekuensi rendah → potensi peningkatan retensi
- Pelanggan loyal memberikan kontribusi signifikan terhadap revenue
