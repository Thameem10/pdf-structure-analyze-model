import json
from pathlib import Path

# ---------------------------------------
# Paths
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_JSON_PATH = BASE_DIR / "data" / "predictions" / "demo_testing_with_predictions.json"

OUTPUT_DIR = BASE_DIR / "data" / "extracted"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_JSON_PATH = OUTPUT_DIR / "structured_sections.json"

# ---------------------------------------
# Load Prediction JSON
# ---------------------------------------

with open(INPUT_JSON_PATH, "r") as f:
    data = json.load(f)

# ---------------------------------------
# Section Order (CHANGE ORDER HERE IF NEEDED)
# ---------------------------------------

SECTION_ORDER = ["Heading", "Subheading", "Paragraph", "Table", "Image"]

# ---------------------------------------
# Build Sections (With Merge Logic)
# ---------------------------------------

sections = []
current_section = None

previous_label = None

for block in data:
    label = block.get("predicted_label")
    content = block.get("content")

    if label not in SECTION_ORDER:
        continue

    # -------------------------
    # Start New Section
    # -------------------------
    if label in ["Heading", "Subheading"]:

        # If same as previous and section exists → merge
        if current_section and label == previous_label:
            if label == "Heading":
                current_section["heading"] += " " + content
            else:
                if current_section["subheading"]:
                    current_section["subheading"] += " " + content
                else:
                    current_section["subheading"] = content

        else:
            if current_section:
                sections.append(current_section)

            current_section = {
                "heading": content if label == "Heading" else None,
                "subheading": content if label == "Subheading" else None,
                "paragraphs": [],
                "tables": [],
                "images": []
            }

    # -------------------------
    # Inside Section
    # -------------------------
    elif current_section:

        # Merge consecutive paragraphs
        if label == "Paragraph":
            if previous_label == "Paragraph" and current_section["paragraphs"]:
                current_section["paragraphs"][-1] += " " + content
            else:
                current_section["paragraphs"].append(content)

        # Merge consecutive tables
        elif label == "Table":
            if previous_label == "Table" and current_section["tables"]:
                current_section["tables"][-1] += " " + content
            else:
                current_section["tables"].append(content)

        # Image ends section
        elif label == "Image":
            current_section["images"].append(content)
            sections.append(current_section)
            current_section = None

    previous_label = label

# Append last section
if current_section:
    sections.append(current_section)
    
    
# ---------------------------------------
# Save Structured JSON
# ---------------------------------------

with open(OUTPUT_JSON_PATH, "w") as f:
    json.dump(sections, f, indent=4)

print(f"\nStructured sections saved to: {OUTPUT_JSON_PATH}")