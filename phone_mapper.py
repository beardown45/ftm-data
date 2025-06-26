
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Phone Mapping Tool (No Middle Names, All Rows)")

uploaded_input = st.file_uploader("Upload Test1 - probate.csv", type=["csv"], key="input")
uploaded_template = st.file_uploader("Upload Test2 - probate template.csv", type=["csv"], key="template")

if uploaded_input and uploaded_template:
    df_input = pd.read_csv(uploaded_input)
    df_template = pd.read_csv(uploaded_template)
    df_output = pd.DataFrame(columns=df_template.columns)

    input_phone_fields = [
        'Wireless 1', 'Wireless 2', 'Wireless 3', 'Wireless 4', 'Wireless 5',
        'Landline 1', 'Landline 2', 'Landline 3', 'Landline 4', 'Landline 5',
        'Wireless 1.1', 'Wireless 2.1', 'Wireless 3.1', 'Wireless 4.1', 'Wireless 5.1',
        'Landline 1.1', 'Landline 2.1', 'Landline 3.1', 'Landline 4.1', 'Landline 5.1'
    ]
    output_phone_fields = [f"Phone {i}" for i in range(1, 21)]
    output_type_fields = [f"Phone Type {i}" for i in range(1, 21)]

    normalized_input_cols = {col.lower().strip(): col for col in df_input.columns}
    total_rows = len(df_input)
    progress = st.progress(0)

    for idx, (_, row) in enumerate(df_input.iterrows()):
        output_row = dict.fromkeys(df_template.columns, "")

        for out_col in df_template.columns:
            key = out_col.lower().strip()
            if key in normalized_input_cols:
                src_col = normalized_input_cols[key]
                output_row[out_col] = row[src_col]

        # Fill full names (first + last only)
        if "Full Name (Deceased)" in df_template.columns:
            fn = row.get("First Name (Deceased)", "")
            ln = row.get("Last Name", "")
            full_name = " ".join(str(part).strip() for part in [fn, ln] if pd.notna(part) and part != "")
            output_row["Full Name (Deceased)"] = full_name

        if "PR Full Name" in df_template.columns:
            fn = row.get("Petitioner First Name", "")
            ln = row.get("Petitioner Last Name", "")
            full_name = " ".join(str(part).strip() for part in [fn, ln] if pd.notna(part) and part != "")
            output_row["PR Full Name"] = full_name

        if "Attorney Full Name" in df_template.columns:
            fn = row.get("Attorney First Name", "")
            ln = row.get("Attorney Last Name", "")
            full_name = " ".join(str(part).strip() for part in [fn, ln] if pd.notna(part) and part != "")
            output_row["Attorney Full Name"] = full_name

        # Phone numbers
        for i, input_col in enumerate(input_phone_fields):
            if input_col in df_input.columns and pd.notna(row[input_col]):
                output_row[output_phone_fields[i]] = row[input_col]
                output_row[output_type_fields[i]] = "mobile" if "Wireless" in input_col else "landline"

        df_output = pd.concat([df_output, pd.DataFrame([output_row])], ignore_index=True)

        # Progress update
        progress.progress((idx + 1) / total_rows)

    st.success(f"Mapping Complete! {len(df_output)} rows processed.")
    st.download_button("Download Mapped File", df_output.to_csv(index=False), file_name="Mapped_Output.csv", mime="text/csv")
