# Proyek Analisis Data: E-Commerce Public Dataset

## Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis data dari E-Commerce Public Dataset. Analisis mencakup proses data wrangling, exploratory data analysis (EDA), hingga pembuatan dashboard interaktif menggunakan Streamlit.

## Struktur Direktori
- **/dashboard**: Berisi file `dashboard.py` dan data yang telah dibersihkan (`main_data.csv`).
- **/data**: Berisi dataset mentah dalam format .csv.
- `Proyek_Analisis_Data_Dini_Arya_Putri.ipynb`: File analisis data lengkap.
- `requirements.txt`: Daftar library Python yang dibutuhkan.

## Cara Menjalankan Dashboard
1. Install library yang dibutuhkan:
   ```bash
   pip install -r requirements.txt

2. Jalankan aplikasi streamlit:
     ```bash
  streamlit run dashboard/dashboard.py

  ### 3. Membuat `requirements.txt`
Karena kamu menggunakan Windows dan kemungkinan besar bekerja di lingkungan lokal, cara paling aman dan bersih adalah menggunakan **pipreqs** atau menulisnya secara manual agar tidak terlalu banyak library yang tidak perlu ikut terbawa.

Jika ingin manual (paling direkomendasikan untuk pemula), isi file `requirements.txt` cukup dengan 4 baris ini:
```text
streamlit
pandas
matplotlib
seaborn
