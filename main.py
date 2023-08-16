import time
import streamlit as st
import pandas as pd
from connector import Sheet


st.set_page_config(page_title="Cari Teman Sekelas", page_icon=":couple:", layout="wide")
JUDUL = st.title("Cari Teman Sekelas")
MATKUL_SI = ["DDP 1","Matdis 1","Kalkulus 1","Manbis","Kombistek"]
MATKUL_IK = ["DDP 1","Matdis 1","Kalkulus 1","PSD"]


def get_user_data():
    """Get user data and selected user name."""
    user_name = st.selectbox("Masukkan Nama Lengkap Kamu", list_of_name)
    user_data = data[data["Nama Mahasiswa"] == user_name].reset_index(drop=True)
    return user_data, user_name


def get_chosen_subject(user_data):
    """Get chosen subjects based on user data."""
    subjects = MATKUL_SI if user_data["Prodi"].values[0][:2] == "SI" else MATKUL_IK
    chosen_subject = RIGHT.multiselect("Pilih Mata Kuliah", subjects)
    return chosen_subject


def compare_student_class(user_data: pd.DataFrame):
    """Compare user's class with another student's class."""
    other_student_name = LEFT.selectbox("Pilih mahasiswa yang ingin dibandingkan", list_of_name)
    other_student_data = data[data["Nama Mahasiswa"] == other_student_name]

    same_class = [subject for subject in set(MATKUL_IK + MATKUL_SI)
                  if user_data[subject].values == other_student_data[subject].values and user_data[subject].values != "-"]

    merged_student_data = pd.concat([user_data, other_student_data]).reset_index(drop=True)
    merged_student_data.index += 1
    return merged_student_data, same_class, other_student_name


def filter_name(name):
    """Filter and format the student's name."""
    prefixes = ["Muh", "Moh", "Moch"]
    first_name, *last_names = name.split()
    return last_names[0] if first_name.startswith(tuple(prefixes)) else first_name


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


def get_review_text():
    try:
        st.subheader("Reviews")
        SHEET_KEY = "1SJbrFnPWD_TLUWkWx9j0VK3qZhYojK241NCr3sABxts"
        sheet = Sheet(SHEET_KEY)

        with st.form(key="feedback_form", clear_on_submit=True):
            review_text = st.text_input("Boleh dong share impression kamu dengan app ini")
            submit_btn = st.form_submit_button("Submit")
            if submit_btn and review_text != "":
                sheet.import_to_sheet(review_text)
                submit_info = st.success("Review telah dikirim!")
                time.sleep(3)
                submit_info.empty()
    except: pass


if __name__ == "__main__":
    data = pd.read_csv("data/processed_data_pembagian_kelas_2023.csv").drop(["NPM"],axis=1).set_index("No").fillna("-")
    list_of_name = sorted(tuple(data["Nama Mahasiswa"].values.tolist()))

    user_data, user_name = get_user_data()
    st.table(user_data)

    LEFT, RIGHT = st.columns(2)

    display_comparison(*compare_student_class(user_data))

    chosen_subject = get_chosen_subject(user_data)
    if chosen_subject != []:
        display_classmate(get_classmate(data, user_data, chosen_subject))
    
    get_review_text()