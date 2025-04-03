import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="📂 File Converter", layout="wide")
st.title("📂 File Converter & Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats.")

files = st.file_uploader("Upload CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        
        try:
            df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)
        except Exception as e:
            st.error(f"Error reading file {file.name}: {e}")
            continue

        if df.empty:
            st.warning(f"{file.name} is empty!")
            continue

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates removed!")
            st.dataframe(df.head())

        if st.checkbox(f"Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include=['number']).mean(), inplace=True)
            st.success("Missing values filled!")
            st.dataframe(df.head())

        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        numeric_columns = df.select_dtypes(include='number').columns.tolist()
        if numeric_columns and st.checkbox(f"Show Chart - {file.name}"):
            selected_chart_column = st.selectbox(f"Select Column for Chart - {file.name}", numeric_columns)
            st.bar_chart(df[selected_chart_column])

        format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
            else:
                df.to_excel(output, index=False, engine='openpyxl')
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            new_name = f"{file.name.split('.')[0]}.{format_choice.lower()}"
            output.seek(0)
            st.download_button("Download File", data=output, file_name=new_name, mime=mime)

st.success("Processing complete!")
