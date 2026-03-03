import json

def remove_footer_rows(input_path, output_path):
    # Load JSON
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Filter out Footer rows
    filtered_data = [
        row for row in data
        if row.get("label") != "Footer"
    ]

    print(f"Original rows: {len(data)}")
    print(f"After removing Footer: {len(filtered_data)}")

    # Save cleaned JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=4)

    print("Footer rows removed successfully!")


# Run it
remove_footer_rows(
    "labelled/features_labeled.json",
    "labelled/features_labeled.json"
)