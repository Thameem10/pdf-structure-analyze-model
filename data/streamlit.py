import streamlit as st
import json

DATA_PATH = "labelled/features_labeled.json"

data = json.load(open(DATA_PATH))

st.title("PDF Line Labeling Tool")

for i, row in enumerate(data):
    st.write(f"Page {row['page_number']}")
    st.write(row["text"])

    row["label"] = st.selectbox(
        "Label",
        ["Heading", "Subheading", "Paragraph", "Footer"],
        index=["Heading", "Subheading", "Paragraph", "Footer"].index(row["label"]) if row["label"] else 2,
        key=i
    )

    st.markdown("---")

if st.button("Save"):
    json.dump(data, open(DATA_PATH, "w"), indent=4)
    st.success("Saved successfully!")