# Men-import library yang diperlukan
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cari Teman Sekelas", page_icon=":couple:", layout="wide")
JUDUL = st.title("Cari Teman Sekelas")

# Membaca dan merapihkan data
data = pd.read_csv("Pembagian-Kelas-Mahasiswa-Angkatan-2022.csv")
data = data.drop(["NPM"],axis=1).set_index("No").fillna("-")

# Membuat data user
nama_list = sorted(tuple(data["Nama Mahasiswa"].values.tolist()))
user_name = st.selectbox("Masukkan Nama Lengkap Kamu", nama_list)
user_data = data[data["Nama Mahasiswa"] == user_name].reset_index(drop=True)

# Mengubah data user ke list
user_list = user_data.values.tolist()

# Merapihkan data user dan menampilkannya
user_data2 = user_data.drop(["PSD"],axis=1) if user_list[0][1][:2] == "SI" else user_data.drop(["Manbis","Kombistek"],axis=1)
user_data2.index += 1
st.table(user_data2)

# Membuat kolom kanan dan kiri
left, right = st.columns(2)

# Meminta list mata kuliah yang diinginkan
matkul_SI = ["DDP 1","Matdis 1","Kalkulus 1","Manbis","Kombistek"]
matkul_IK = ["DDP 1","Matdis 1","Kalkulus 1","PSD"]
matkul = matkul_SI if user_list[0][1][:2] == "SI" else matkul_IK
mata_kuliah = right.multiselect("Pilih Mata Kuliah", matkul)

# Meminta nama mahasiswa yang ingin dibandingkan
target_name = left.selectbox("Pilih mahasiswa yang ingin dibandingkan", nama_list)
target_data = data[data["Nama Mahasiswa"] == target_name]

# Mengubah data target ke dictionary
target_dict = target_data[matkul_IK + ["Manbis","Kombistek"]].to_dict("records")[0]

# Menggabungkan data user dengan mahasiswa yang dibandingkan
compare_data = pd.concat([user_data, target_data]).reset_index(drop=True)
compare_data.index += 1

# Nilai awal
custom_data, check = "", 0

# Menghitung kelas mata kuliah yang sama antara user dengan target
matkul_sama = [b for a,b in zip(user_list[0][2:], target_dict) if a != "-" and a == target_dict[b]]

matkul_sama2 = ", ".join(matkul_sama)

# Membuat fungsi untuk menampilkan data mahasiswa yang memiliki persamaan tipe kelas dengan user
def similarity(pelajaran, df):
    num = (matkul_IK + ["Manbis","Kombistek"]).index(pelajaran) + 2
    return df[df[pelajaran] == user_list[0][num]]

# Merapihkan data sesuai dengan fungsi "similarity"
for value in mata_kuliah:
    if check == 0:
        df = similarity(value, data)
        custom_data = df.drop(df[df["Nama Mahasiswa"] == user_name].index)
        check += 1
    else:
        custom_data = similarity(value, custom_data)

# Memanggil nama target
def filter_name(name):
    res, a = name.split(), ["Muh","Moh","Moch"]
    for value in a:
        if res[0].startswith(value):
            return res[1]
    return res[0]

# tampilan kiri
if target_name == user_name:
    pass
elif len(matkul_sama) > 0:
    if len(matkul_sama) == 1:
        left.markdown(f"Kamu dan {filter_name(target_name)} hanya memiliki **{len(matkul_sama)} kelas matkul** yang sama, yaitu pada matkul:")
    else:
        left.markdown(f"Kamu dan {filter_name(target_name)} memiliki **{len(matkul_sama)} kelas matkul** yang sama, yaitu pada matkul:")
    left.markdown(f"\t**{matkul_sama2}**")
    left.table(compare_data)
elif len(matkul_sama) == 0:
    left.markdown(f"Kamu dan {filter_name(target_name)} tidak memiliki kelas matkul yang sama :(")

<<<<<<< HEAD
def get_classmate(classmate_data, user_data, chosen_subject):
    """Get classmates based on selected subjects."""
    for col in user_data.drop(["Nama Mahasiswa", "Prodi"], axis=1).columns:
        if user_data[col].values[0] != "-" and col in chosen_subject:
            classmate_data = classmate_data[classmate_data[col] == user_data[col].values[0]]
    return classmate_data[classmate_data["Nama Mahasiswa"] != user_data["Nama Mahasiswa"][0]]


def display_comparison(merged_student_data, same_class, target_name):
    """Display comparison of class and common subjects between two students."""
    if len(same_class) > 0 and target_name != user_name:
        if len(same_class) == 1:
            LEFT.markdown(f"Kamu dan {filter_name(target_name)} hanya memiliki **{len(same_class)} kelas matkul** yang sama, yaitu pada matkul:")
        else:
            LEFT.markdown(f"Kamu dan {filter_name(target_name)} memiliki **{len(same_class)} kelas matkul** yang sama, yaitu pada matkul:")
        LEFT.markdown(f"\t**{', '.join(same_class)}**")
        LEFT.table(merged_student_data)
    elif len(same_class) == 0 and target_name != user_name:
        LEFT.markdown(f"Kamu dan {filter_name(target_name)} tidak memiliki kelas matkul yang sama :(")


def display_classmate(classmate_data):
    """Display classmates' data."""
    RIGHT.markdown(f"Ada **{classmate_data.shape[0]} mahasiswa** yang sekelas dengan Kamu")
    classmate_data = classmate_data.sort_values(by=["Nama Mahasiswa"]).reset_index(drop=True)
    classmate_data.index += 1
    RIGHT.table(classmate_data)


if __name__ == "__main__":
    data = pd.read_csv("Pembagian-Kelas-Mahasiswa-Angkatan-2022.csv").drop(["NPM"],axis=1).set_index("No").fillna("-")
    list_of_name = sorted(tuple(data["Nama Mahasiswa"].values.tolist()))

    user_data, user_name = get_user_data()
    st.table(user_data)

    LEFT, RIGHT = st.columns(2)

    display_comparison(*compare_student_class(user_data))

    chosen_subject = get_chosen_subject(user_data)
    if chosen_subject != []:
        display_classmate(get_classmate(data, user_data, chosen_subject))
=======
# tampilan kanan
if mata_kuliah != []:
    right.markdown(f"Ada **{custom_data.shape[0]} mahasiswa** yang sekelas dengan Kamu")
    custom_data = custom_data.sort_values(by=["Nama Mahasiswa"]).reset_index(drop=True)
    custom_data.index += 1
    right.table(custom_data)
>>>>>>> parent of 05109c6 (update main.py)
