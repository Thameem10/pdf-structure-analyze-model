import json

def auto_label(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for row in data:
        if row["font_size_relative"] > 1.4 and row["is_bold"]:
            row["label"] = "Heading"
        elif row["font_size_relative"] > 1.1 and row["is_bold"]:
            row["label"] = "Subheading"
        else:
            row["label"] = "Paragraph"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Auto labeling complete")

auto_label("interim/features.json", "labelled/features_labeled.json")