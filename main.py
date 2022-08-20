# Men-import library yang diperlukan
import plotly.express as px
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cari Teman Sekelas", page_icon=":couple:", layout="wide")
JUDUL = st.title("Cari Teman Sekelas")

# Membaca dan merapihkan data
data = pd.read_csv("Pembagian-Kelas-Mahasiswa-Angkatan-2022.csv")
data = data.drop(["NPM"],axis=1).set_index("No")
data = data.fillna("-")

# Membuat list nama mahasiswa dan menampilkan data mahasiswa tersebut
nama_list = sorted(tuple(data["Nama Mahasiswa"].values.tolist()))
nama = st.selectbox("Masukkan Nama Lengkap Kamu", nama_list)
data_user = data[data["Nama Mahasiswa"] == nama]
st.table(data_user.reset_index(drop=True))

# Meminta list mata kuliah yang diinginkan
matkul = ["DDP 1","Matdis 1","Kalkulus 1","PSD","Manbis","Kombistek"]
mata_kuliah = st.multiselect("Pilih Mata Kuliah", matkul)

# Mengubah data user ke dalam bentuk list
data_user = data_user.values.tolist()

# Nilai awal
custom_data, check = "", 0

# Membuat fungsi untuk menampilkan data mahasiswa yang memiliki persamaan tipe kelas dengan user
def similarity(pelajaran, df):
    num = matkul.index(pelajaran) + 2
    return df[df[pelajaran] == data_user[0][num]]

# Merapihkan data sesuai dengan fungsi "similarity"
for value in mata_kuliah:
    if check == 0:
        df = similarity(value, data)
        custom_data = df.drop(df[df["Nama Mahasiswa"] == nama].index)
        check += 1
    else:
        custom_data = similarity(value, custom_data)

def visual_pie(df):
    df["Kelas"] = df["Prodi"].str[3:]
    df["Kelas"] = df["Kelas"].apply(lambda x: "Reguler" if x == "Reg" else "Paralel")
    df["Prodi"] = df["Prodi"].str[:2]
    path_cols = ["Prodi","Kelas"]

    fig = px.sunburst(data_frame=df, path=path_cols, maxdepth=-1,
                      color_discrete_sequence=px.colors.qualitative.Pastel)
    return fig


# Membuat tombol untuk menampilkan data
tampilkan = st.button("Show")

# Mencoba menampilkan data
try:
    if tampilkan:
        st.subheader(f"Ada {custom_data.shape[0]} teman yang sekelas dengan Kamu")
        left, right = st.columns(2)
        left.table(custom_data.sort_values(by=["Nama Mahasiswa"]).reset_index(drop=True))
        right.plotly_chart(visual_pie(custom_data), use_container_width=True)

# Memunculkan exception bila terdapat kolom yang belum diisi
except:
    st.error("Mohon isi kolom di atas.")
