import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Mengatur gaya visualisasi
sns.set(style="whitegrid")

# Judul Dashboard
st.title("Dashboard Penyewaan Sepeda 🚴‍♂️")

# Memuat dataset
@st.cache  # Caching untuk meningkatkan performa
def load_data():
    day_df = pd.read_csv('day.csv')  # Ganti dengan path Anda
    hour_df = pd.read_csv('hour.csv')  # Ganti dengan path Anda
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])  # Mengonversi kolom tanggal
    return day_df, hour_df

day_df, hour_df = load_data()

# Menampilkan informasi umum tentang dataset
st.subheader("Informasi Pengguna Harian")
casual_users = day_df['casual'].sum()
registered_users = day_df['registered'].sum()
total_users = casual_users + registered_users

st.write(f"**Pengguna Kasual**: {casual_users}")
st.write(f"**Pengguna Terdaftar**: {registered_users}")
st.write(f"**Total Pengguna**: {total_users}")

# Visualisasi Distribusi Total Penyewaan Sepeda per Bulan
st.subheader("Distribusi Total Penyewaan Sepeda per Bulan")
day_df['month'] = day_df['dteday'].dt.month_name()  # Mengambil nama bulan
monthly_rentals = day_df.groupby('month')['cnt'].sum().reindex(
    ['January', 'February', 'March', 'April', 'May', 'June', 
     'July', 'August', 'September', 'October', 'November', 'December']
)

# Membuat figure untuk monthly rentals
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(x=monthly_rentals.index, y=monthly_rentals.values, palette='Blues', ax=ax1)
ax1.set_title('Distribusi Total Penyewaan Sepeda per Bulan')
ax1.set_xlabel('Bulan')
ax1.set_ylabel('Total Penyewaan')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)

st.pyplot(fig1)

# Visualisasi Penyewaan Berdasarkan Musim
st.subheader("Penyewaan Berdasarkan Musim")
seasonal_rentals = day_df.groupby('season')['cnt'].sum()

# Membuat figure untuk seasonal rentals
fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.barplot(x=seasonal_rentals.index, y=seasonal_rentals.values, palette='Oranges', ax=ax2)
ax2.set_title('Penyewaan Berdasarkan Musim')
ax2.set_xlabel('Musim')
ax2.set_ylabel('Total Penyewaan')

st.pyplot(fig2)

# Visualisasi Pengaruh Cuaca terhadap Penyewaan
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
weather_conditions = {
    1: 'Jelas, Beberapa Awan',
    2: 'Kabut, Beberapa Awan, Hujan Ringan',
    3: 'Awan Tebal',
    4: 'Hujan Berat, Hujan Es'
}
day_df['kondisi_cuaca'] = day_df['weathersit'].map(weather_conditions)

weather_effect = day_df.groupby('kondisi_cuaca')['cnt'].mean().reset_index()

# Membuat figure untuk weather effect
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(data=weather_effect, x='kondisi_cuaca', y='cnt', palette='Greens', ax=ax3)
ax3.set_title('Pengaruh Cuaca terhadap Penyewaan Sepeda')
ax3.set_xlabel('Kondisi Cuaca')
ax3.set_ylabel('Rata-rata Penyewaan')

for index, row in weather_effect.iterrows():
    ax3.text(index, row['cnt'], round(row['cnt'], 2), color='black', ha="center")

st.pyplot(fig3)

# Visualisasi Perbandingan Penggunaan Sepeda antara Tahun 2011 dan 2012
st.subheader("Perbandingan Penggunaan Sepeda antara Tahun 2011 dan 2012")
day_df['year'] = day_df['dteday'].dt.year  # Menambahkan kolom tahun

yearly_rentals = day_df.groupby('year')['cnt'].sum()

# Membuat figure untuk yearly rentals
fig4, ax4 = plt.subplots(figsize=(8, 5))
sns.barplot(x=yearly_rentals.index.astype(str), y=yearly_rentals.values, palette='Purples', ax=ax4)
ax4.set_title('Total Penyewaan Sepeda per Tahun')
ax4.set_xlabel('Tahun')
ax4.set_ylabel('Total Penyewaan')

st.pyplot(fig4)

# Analisis Clustering: Manual Grouping
st.subheader("Analisis Clustering: Manual Grouping")
# Mengelompokkan penyewaan ke dalam kategori berdasarkan jumlah
def manual_grouping(row):
    if row['cnt'] < 100:
        return 'Rendah'
    elif 100 <= row['cnt'] < 300:
        return 'Sedang'
    else:
        return 'Tinggi'

day_df['manual_group'] = day_df.apply(manual_grouping, axis=1)
manual_group_counts = day_df['manual_group'].value_counts()

# Membuat figure untuk manual grouping
fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.barplot(x=manual_group_counts.index, y=manual_group_counts.values, palette='Blues', ax=ax5)
ax5.set_title('Manual Grouping Penyewaan Sepeda')
ax5.set_xlabel('Kategori Penyewaan')
ax5.set_ylabel('Jumlah Penyewaan')

st.pyplot(fig5)

# Analisis Clustering: Binning
st.subheader("Analisis Clustering: Binning")
# Mengelompokkan data berdasarkan total penyewaan
day_df['rental_category'] = pd.cut(day_df['cnt'], bins=[0, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000], 
                                   labels=['0-50', '51-100', '101-200', '201-300', '301-400', '401-500', '501-600', '601-700', '701-800', '801-900', '901-1000'])

# Menghitung jumlah penyewaan dalam setiap kategori
clustering_counts = day_df['rental_category'].value_counts().sort_index()

# Membuat figure untuk binning
fig6, ax6 = plt.subplots(figsize=(10, 6))
sns.barplot(x=clustering_counts.index, y=clustering_counts.values, palette='Oranges', ax=ax6)
ax6.set_title('Binning Penyewaan Sepeda berdasarkan Jumlah Penyewaan')
ax6.set_xlabel('Kategori Penyewaan')
ax6.set_ylabel('Jumlah Penyewaan')

st.pyplot(fig6)

# Menampilkan rentang waktu
st.sidebar.header("Rentang Waktu")
start_date = st.sidebar.date_input("Mulai", value=pd.to_datetime('2011-01-01'))
end_date = st.sidebar.date_input("Selesai", value=pd.to_datetime('2012-12-31'))

# Pastikan start_date dan end_date bertipe datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data berdasarkan rentang waktu yang dipilih
filtered_data = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date)]
st.write("Data yang difilter berdasarkan rentang waktu:")
st.write(filtered_data)

# Copyright
st.write("Copyright (c) Your Name 2023")
