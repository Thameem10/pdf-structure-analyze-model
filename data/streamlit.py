import streamlit as st
import json
import os
import pandas as pd

DATA_PATH = "labelled/features_labeled.json"
LABEL_OPTIONS = ["Heading", "Subheading", "Paragraph", "Footer", "Image", "Table"]


# ----------------------------
# Load & Save
# ----------------------------
def load_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def export_csv(data):
    df = pd.DataFrame(data)
    csv_path = "labelled/features_labeled.csv"
    df.to_csv(csv_path, index=False)
    return csv_path


# ----------------------------
# Auto Label
# ----------------------------
def auto_label_rows(data):

    for row in data:

        if row["type"] == "Image":
            row["label"] = "Image"

        elif row["type"] == "Table":
            row["label"] = "Table"

        elif row["type"] == "Text":

            if row["font_size_relative"] > 1.4 and row["is_bold"]:
                row["label"] = "Heading"

            elif row["font_size_relative"] > 1.1 and row["is_bold"]:
                row["label"] = "Subheading"

            elif row["text_length"] < 40 and row["y_position"] > 750:
                row["label"] = "Footer"

            else:
                row["label"] = "Paragraph"

    return data


# ----------------------------
# Streamlit UI
# ----------------------------

st.title("📄 PDF Line Labeling Tool")

if "data" not in st.session_state:
    st.session_state.data = load_data()

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Auto Label"):
        st.session_state.data = auto_label_rows(st.session_state.data)
        st.success("Auto labeling applied!")

with col2:
    if st.button("💾 Save JSON"):
        save_data(st.session_state.data)
        st.success("Saved successfully!")

with col3:
    if st.button("📤 Export CSV"):
        path = export_csv(st.session_state.data)
        st.success(f"Exported to {path}")

st.markdown("---")


# ----------------------------
# Labeling Interface
# ----------------------------

for i, row in enumerate(st.session_state.data):

    st.write(f"### Page {row['page_number']}")

    # Handle text safely
    if row["type"] == "Text":
        st.write(row.get("text", ""))

    elif row["type"] == "Image":
        st.info(f"🖼 Image | Area: {row.get('image_area', 0)}")

    elif row["type"] == "Table":
        st.info(
            f"📊 Table | Rows: {row.get('table_rows', 0)} "
            f"| Columns: {row.get('table_columns', 0)}"
        )

    current_label = row.get("label", "Paragraph")

    row["label"] = st.selectbox(
        "Label",
        LABEL_OPTIONS,
        index=LABEL_OPTIONS.index(current_label)
        if current_label in LABEL_OPTIONS else 2,
        key=f"label_{i}"
    )

    st.markdown("---")