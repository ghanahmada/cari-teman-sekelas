# Men-import library yang diperlukan
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
user_name = st.selectbox("Masukkan Nama Lengkap Kamu", nama_list)
user_data = data[data["Nama Mahasiswa"] == user_name]
st.table(user_data.reset_index(drop=True))

# Membuat kolom kanan dan kiri
left, right = st.columns(2)

# Meminta list mata kuliah yang diinginkan
matkul = ["DDP 1","Matdis 1","Kalkulus 1","PSD","Manbis","Kombistek"]
mata_kuliah = left.multiselect("Pilih Mata Kuliah", matkul)

# Meminta nama mahasiswa yang ingin dibandingkan
target_name = right.selectbox("Pilih mahasiswa yang ingin dibandingkan", nama_list)
target_data = data[data["Nama Mahasiswa"] == target_name]

# Nilai awal
matkul_sama, custom_data, check = [], "", 0

# Mengubah data user ke list dan data target ke dictionary
user_list = user_data.values.tolist()
target_dict = target_data[matkul].to_dict("records")[0]

# Menghitung kelas mata kuliah yang sama antara user dengan target
for a, b in zip(user_list[0][2:], target_dict):
    if a != "-":
        if a == target_dict[b]:
            matkul_sama.append(b)

matkul_sama2 = ", ".join(matkul_sama)

# Membuat fungsi untuk menampilkan data mahasiswa yang memiliki persamaan tipe kelas dengan user
def similarity(pelajaran, df):
    num = matkul.index(pelajaran) + 2
    return df[df[pelajaran] == user_list[0][num]]

# Merapihkan data sesuai dengan fungsi "similarity"
for value in mata_kuliah:
    if check == 0:
        df = similarity(value, data)
        custom_data = df.drop(df[df["Nama Mahasiswa"] == user_name].index)
        check += 1
    else:
        custom_data = similarity(value, custom_data)

# Menampilkan data
if target_name == user_name:
    pass
elif len(matkul_sama) > 0:
    right.markdown(f"Kamu dan {target_name.split()[0]} memiliki **{len(matkul_sama)} kelas matkul** yang sama, yaitu pada matkul:")
    right.markdown(f"\t**{matkul_sama2}**")
    right.table(target_data.reset_index(drop=True))
elif len(matkul_sama) == 0:
    right.markdown(f"Kamu dan {target_name.split()[0]} tidak memiliki kelas matkul yang sama :(")

if mata_kuliah != []:
    left.markdown(f"Ada **{custom_data.shape[0]} mahasiswa** yang sekelas dengan Kamu")
    left.table(custom_data.sort_values(by=["Nama Mahasiswa"]).reset_index(drop=True))
