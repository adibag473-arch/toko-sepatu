import streamlit as st
import pandas as pd

# 1. Mengatur Judul Tab Browser dan Layout Website
st.set_page_config(page_title="SneakerStation | Katalog Sepatu", layout="wide", page_icon="👟")

# 2. Membuat Bagian Header / Judul Website
st.title("👟 SneakerStation Marketplace")
st.write("Selamat datang! Silakan lihat katalog sepatu original dan terbaru kami di bawah ini.")
st.markdown("---")

# 3. Membaca Database CSV Sepatu
try:
    df = pd.read_csv("data_sepatu1rev.csv")
except FileNotFoundError:
    st.error("Waduh! File 'data_sepatu1rev.csv' tidak ditemukan. Pastikan posisinya sudah benar di dalam folder.")
    st.stop()

# 4. Membuat Menu Samping (Sidebar) untuk Pencarian & Filter
st.sidebar.header("🔍 Filter Pencarian")
search_query = st.sidebar.text_input("Cari nama sepatu:", "")

# Mengambil daftar kategori sepatu secara otomatis untuk menu pilihan
kategori_list = ["Semua Kategori"] + list(df["Kategori"].unique())
selected_kategori = st.sidebar.selectbox("Pilih Kategori Sepatu:", kategori_list)

# Proses Penyaringan Data Sepatu
filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[filtered_df["Nama"].str.contains(search_query, case=False)]
if selected_kategori != "Semua Kategori":
    filtered_df = filtered_df[filtered_df["Kategori"] == selected_kategori]

# 5. Menampilkan Produk di Halaman Utama (Bentuk Grid/Kolom)
if filtered_df.empty:
    st.warning("Maaf, sepatu yang Anda cari tidak ditemukan. Coba gunakan kata kunci lain!")
else:
    # Membuat susunan layout 3 kolom sejajar
    cols = st.columns(3)
    
    for index, row in filtered_df.iterrows():
        # Mengatur agar produk otomatis terbagi rata ke kolom 1, 2, dan 3
        col_idx = index % 3
        with cols[col_idx]:
            # Membuat kotak pembungkus (box container) agar tampilan rapi
            with st.container(border=True):
                # Menampilkan Foto Sepatu
                try:
                    st.image(row["Foto"], use_container_width=True)
                except:
                    # Jika foto rusak/tidak ketemu, gunakan gambar tiruan sementara
                    st.image("https://via.placeholder.com/300", caption="Foto Tidak Tersedia", use_container_width=True)
                
                # Menampilkan Informasi Detail Sepatu
                st.subheader(row["Nama"])
                st.caption(f"Kategori: {row['Kategori']}")
                
                # Mengubah format angka harga menjadi format Rupiah (contoh: Rp 950.000)
                harga_rupiah = f"Rp {row['Harga']:,}".replace(",", ".")
                st.write(f"**Harga:** {harga_rupiah}")
                
                # Menampilkan Status Stok dengan Label Berwarna
                if row["Status"] == "Tersedia":
                    st.success(f"🟢 {row['Status']}")
                elif row["Status"] == "Stok Sedikit":
                    st.warning(f"🟡 {row['Status']}")
                else:
                    st.error(f"🔴 {row['Status']}")
                
                # Tombol Beli
                st.button("Beli Sekarang", key=f"btn_{index}")