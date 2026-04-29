import streamlit as st
import pandas as pd

st.title("مقارنة كشف البيانات")

file1 = st.file_uploader("ارفع الداتاسيت الأولى", type=["xlsx", "csv"])
file2 = st.file_uploader("ارفع الداتاسيت الثانية", type=["xlsx", "csv"])

def load_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file).astype(str)
    else:
        return pd.read_excel(file).astype(str)

if file1 and file2:

    df1 = load_file(file1)
    df2 = load_file(file2)

    st.success("تم تحميل الملفات")

    # 🔹 تختار العمود بنفسك
    col = st.selectbox("اختار عمود اسم الموظف:", df1.columns)

    set1 = set(df1[col].dropna())
    set2 = set(df2[col].dropna())

    # العمليات
    مشتركون = set1 & set2
    فقط_الأولى = set1 - set2
    فقط_الثانية = set2 - set1

    # تحويل إلى DataFrame
    df_common = pd.DataFrame(list(مشتركون), columns=["الرقم الوظيفي"])
    df_only1 = pd.DataFrame(list(فقط_الأولى), columns=["الرقم الوظيفي"])
    df_only2 = pd.DataFrame(list(فقط_الثانية), columns=["الرقم الوظيفي"])

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "المشتركون",
        "في الأولى فقط",
        "في الثانية فقط",
        "ملخص"
    ])

    # 🔹 التاب 1
    with tab1:
        st.subheader("الموظفين المشتركين")
        st.dataframe(df_common, use_container_width=True)

    # 🔹 التاب 2
    with tab2:
        st.subheader("الموظفين في الداتاسيت الأولى فقط")
        st.dataframe(df_only1, use_container_width=True)

    # 🔹 التاب 3
    with tab3:
        st.subheader("الموظفين في الداتاسيت الثانية فقط")
        st.dataframe(df_only2, use_container_width=True)

    # 🔹 التاب 4 (الملخص)
    with tab4:
        st.subheader("ملخص الأعداد")

        summary = pd.DataFrame({
            "الفئة": ["مشتركون", "في الأولى فقط", "في الثانية فقط"],
            "العدد": [len(مشتركون), len(فقط_الأولى), len(فقط_الثانية)]
        })

        st.dataframe(summary, use_container_width=True)
