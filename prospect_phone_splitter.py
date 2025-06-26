
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Prospect Phone Splitter")

uploaded_file = st.file_uploader("Upload Prospect CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    phone_cols = [col for col in df.columns if 'phone' in col.lower()]

    if not phone_cols:
        st.error("No phone columns found in the uploaded file.")
    else:
        expanded_rows = []
        for _, row in df.iterrows():
            for phone_col in phone_cols:
                phone_number = row[phone_col]
                if pd.notna(phone_number):
                    new_row = row.copy()
                    new_row['Phone'] = phone_number
                    expanded_rows.append(new_row.drop(phone_cols))

        if expanded_rows:
            df_expanded = pd.DataFrame(expanded_rows)
            st.success(f"Processed {len(df)} prospects into {len(df_expanded)} rows.")
            st.download_button("Download Expanded File", df_expanded.to_csv(index=False), file_name="expanded_prospects.csv", mime="text/csv")
        else:
            st.warning("No valid phone numbers found in the uploaded file.")
