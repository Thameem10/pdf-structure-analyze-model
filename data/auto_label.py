import json


def auto_label_rows(data):
    for i, row in enumerate(data):

        if row["type"] == "Image":
            row["label"] = "Image"
            continue

        if row["type"] == "Table":
            row["label"] = "Table"
            continue

        if row["type"] != "Text":
            continue

        # Heading
        if row["font_size_relative"] > 1.5 or row["is_bold"]:
            row["label"] = "Heading"

        # Subheading
        elif (
            row["is_bold"]
            and row["word_count"] <= 10
        ):
            row["label"] = "Subheading"

        # Footer
        elif row["text_length"] < 40 and row["y_position"] > 750:
            row["label"] = "Footer"

        # Paragraph
        elif (
            row["word_count"] > 15
            or row["ends_with_period"] == 1
            or row["punctuation_ratio"] > 0.0001
        ):
            row["label"] = "Paragraph"

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