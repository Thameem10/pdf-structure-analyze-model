import json


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


def auto_label_file(input_path, output_path):
    """
    Load features → auto label → save labeled output.
    """

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    labeled_data = auto_label_rows(data)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(labeled_data, f, indent=4)

    print("Auto labeling complete!")

auto_label_file("interim/features.json", "labelled/features_labeled.json")