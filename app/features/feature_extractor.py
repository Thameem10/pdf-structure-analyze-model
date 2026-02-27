from typing import List, Dict

from app.features.feature_utils import (
    is_bold,
    uppercase_ratio,
    contains_numbering,
    text_length,
)


class FeatureExtractor:
    """
    Extracts features from multi-type layout elements:
    Text, Image, Table
    """

    def __init__(self, layout_elements: List[Dict]):
        self.layout_elements = layout_elements

    def extract(self) -> List[Dict]:

        all_features = []

        # --- Compute average font size for entire document (Text only) ---
        font_sizes = [
            el.get("font_size")
            for el in self.layout_elements
            if el.get("type") == "Text" and el.get("font_size") is not None
        ]

        avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else 1

        for element in self.layout_elements:

            element_type = element.get("type")

            # --------------------------------------------------
            # TEXT FEATURES
            # --------------------------------------------------
            if element_type == "Text":

                line_text = element.get("content", "")
                max_font_size = element.get("font_size", 0)
                bold_flag = element.get("is_bold", 0)

                feature_row = {
                    "type": "Text",
                    "page_number": element.get("page_number"),
                    "content": line_text,
                    # --- Typography ---
                    "font_size": max_font_size,
                    "font_size_relative": max_font_size / avg_font_size if avg_font_size else 0,
                    "is_bold": bold_flag,

                    # --- Text ---
                    "uppercase_ratio": uppercase_ratio(line_text),
                    "text_length": text_length(line_text),
                    "contains_numbering": contains_numbering(line_text),

                    # --- Layout ---
                    "y_position": element.get("y_position", 0),
                    "block_width": element.get("block_width", 0),

                    # --- Image/Table placeholders ---
                    "image_area": 0,
                    "table_rows": 0,
                    "table_columns": 0,

                    "label": None
                }

                all_features.append(feature_row)

            # --------------------------------------------------
            # IMAGE FEATURES
            # --------------------------------------------------
            elif element_type == "Image":

                feature_row = {
                    "type": "Image",
                    "page_number": element.get("page_number"),
                    "content": element.get("content"),

                    # --- No typography ---
                    "font_size": 0,
                    "font_size_relative": 0,
                    "is_bold": 0,

                    # --- No text ---
                    "uppercase_ratio": 0,
                    "text_length": 0,
                    "contains_numbering": 0,

                    # --- Layout ---
                    "y_position": element.get("y_position", 0),
                    "block_width": element.get("width", 0),

                    # --- Image features ---
                    "image_area": element.get("area", 0),
                    "image_aspect_ratio": element.get("aspect_ratio", 0),

                    # --- Table placeholders ---
                    "table_rows": 0,
                    "table_columns": 0,

                    "label": None
                }

                all_features.append(feature_row)

            # --------------------------------------------------
            # TABLE FEATURES
            # --------------------------------------------------
            elif element_type == "Table":

                feature_row = {
                    "type": "Table",
                    "page_number": element.get("page_number"),
                    "content": element.get("content"),

                    # --- No typography ---
                    "font_size": 0,
                    "font_size_relative": 0,
                    "is_bold": 0,

                    # --- No text ---
                    "uppercase_ratio": 0,
                    "text_length": 0,
                    "contains_numbering": 0,

                    # --- Layout ---
                    "y_position": element.get("y_position", 0),
                    "block_width": element.get("width", 0),

                    # --- Image placeholder ---
                    "image_area": 0,

                    # --- Table features ---
                    "table_rows": element.get("rows", 0),
                    "table_columns": element.get("columns", 0),

                    "label": None
                }

                all_features.append(feature_row)

        return all_features