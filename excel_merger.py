import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Robust Excel Merger for Probate Files")
st.markdown("Upload multiple CSV files below. They will be merged into one Excel file with all columns aligned.")

uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)

def deduplicate_columns(columns):
    seen = {}
    new_cols = []
    for col in columns:
        col = col if isinstance(col, str) else str(col)
        if col not in seen:
            seen[col] = 1
            new_cols.append(col)
        else:
            seen[col] += 1
            new_cols.append(f"{col}.{seen[col]}")
    return new_cols

if uploaded_files:
    all_dfs = []

    for file in uploaded_files:
        try:
            df = pd.read_csv(file)

            df.columns = deduplicate_columns(df.columns)

            # Normalize phone fields (no .1's)
            df.columns = [
                col.replace("Wireless 1.1", "Wireless 1")
                   .replace("Wireless 2.1", "Wireless 2")
                   .replace("Wireless 3.1", "Wireless 3")
                   .replace("Wireless 4.1", "Wireless 4")
                   .replace("Wireless 5.1", "Wireless 5")
                   .replace("Landline 1.1", "Landline 1")
                   .replace("Landline 2.1", "Landline 2")
                   .replace("Landline 3.1", "Landline 3")
                   .replace("Landline 4.1", "Landline 4")
                   .replace("Landline 5.1", "Landline 5")
                for col in df.columns
            ]

            all_dfs.append(df)

        except Exception as e:
            st.error(f"Error reading file '{file.name}': {e}")

    if all_dfs:
        # Outer join merge to preserve all columns from all files
        merged_df = pd.concat(all_dfs, axis=0, join="outer", ignore_index=True)

        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            return output.getvalue()

        st.success("Files merged successfully! Download your file below.")
        st.download_button(
            label="Download Merged Excel File",
            data=to_excel(merged_df),
            file_name="Merged_Probate_Data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
