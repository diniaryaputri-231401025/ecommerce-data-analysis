# 🛒 E-Commerce Public Data Analysis Dashboard

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org/)

Proyek ini adalah submission akhir untuk kelas **Belajar Analisis Data dengan Python** dari Dicoding. Fokus utama proyek ini adalah menganalisis *E-Commerce Public Dataset* asal Brazil untuk menggali *business insight* yang relevan, serta membangun *interactive dashboard* menggunakan Streamlit.

## 👤 Profil
- **Nama:** Dini Arya Putri
- **Email:** diniarya135@gmail.com
- **ID Dicoding:** CDCC319D6X1000

## ❓ Pertanyaan Bisnis
Analisis ini dibuat untuk menjawab pertanyaan bisnis berikut:
1. Bagaimana performa penjualan dan revenue perusahaan dalam beberapa bulan terakhir?
2. Produk apa yang memiliki performa terbaik dan terburuk berdasarkan jumlah penjualan?
3. Bagaimana distribusi pelanggan berdasarkan wilayah (state)?
4. Bagaimana segmentasi pelanggan berdasarkan perilaku transaksi menggunakan analisis RFM (Recency, Frequency, Monetary)?
5. Bagaimana hubungan antara frekuensi transaksi dan total pengeluaran pelanggan?

## ✨ Teknik Analisis Lanjutan yang Diterapkan
Untuk mendapatkan *insight* yang lebih dalam dan komprehensif, proyek ini menerapkan beberapa teknik analisis lanjutan (tanpa algoritma *Machine Learning*):

1. **RFM Analysis:** Mengukur perilaku pelanggan berdasarkan tiga metrik utama:
   - **Recency:** Berapa hari sejak pelanggan terakhir kali berbelanja.
   - **Frequency:** Berapa kali pelanggan melakukan transaksi.
   - **Monetary:** Berapa total uang yang dihabiskan pelanggan.
2. **Customer Segmentation (Manual Clustering):** Melakukan *grouping* secara manual berdasarkan skor RFM untuk membagi pelanggan ke dalam beberapa segmen (contoh: *Loyal Customer*, *Recent Customer*, *Standard*, dan *At Risk*). Hal ini membantu tim *marketing* untuk melakukan promosi yang lebih tertarget.
3. **Geospatial / Demographics Analysis:** Menganalisis sebaran pelanggan berdasarkan lokasi geografis (State/Negara Bagian) untuk mengetahui wilayah dengan basis pelanggan terbesar.

## 📁 Struktur Direktori
```text
ecommerce-data-analysis/
│
├── dashboard/
│   ├── dashboard.py       # Source code untuk Streamlit dashboard
│   └── all_data.csv       # Dataset yang sudah dibersihkan dan digabung
│
├── data/                  # Folder berisi seluruh dataset mentah (.csv)
│
├── Proyek_Analisis_Data_Dini_Arya_Putri.ipynb  # Notebook analisis utama (Data Wrangling, EDA, Visualization)
├── README.md              # Dokumentasi proyek
├── requirements.txt       # Daftar library Python yang dibutuhkan
└── url.txt                # Tautan menuju dashboard yang telah di-deploy
```

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
