import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cari Teman Sekelas", page_icon=":couple:", layout="wide")
JUDUL = st.title("Cari Teman Sekelas")

data = pd.read_csv("Pembagian-Kelas-Mahasiswa-Angkatan-2022.csv")
data = data.drop(["NPM"],axis=1).set_index("No")
data = data.fillna("-")

nama_list = sorted(tuple(data["Nama Mahasiswa"].values.tolist()))
matkul = ["DDP 1","Matdis 1","Kalkulus 1","PSD","Manbis","Kombistek"]

nama = st.selectbox("Masukkan Nama Lengkap Kamu", nama_list)
data_user = data[data["Nama Mahasiswa"] == nama]
st.table(data_user.reset_index(drop=True))

mata_kuliah = st.multiselect("Pilih Mata Kuliah", matkul)

data_user = data_user.values.tolist()
custom_data, check = "", 0

def similarity(pelajaran, df):
    num = matkul.index(pelajaran) + 2
    return df[df[pelajaran] == data_user[0][num]]

for value in mata_kuliah:
    if check == 0:
        custom_data = similarity(value, data)
    else:
        custom_data = similarity(value, custom_data)
    check += 1

tampilkan = st.button("Show")

try:
    if tampilkan:
        st.table(custom_data.reset_index(drop=True))

except:
    st.error("Mohon isi kolom di atas.")
