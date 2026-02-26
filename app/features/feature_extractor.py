from typing import List, Dict
from statistics import mean

from app.features.feature_utils import (
    is_bold,
    uppercase_ratio,
    contains_numbering,
    text_length,
)


class FeatureExtractor:
    """
    Converts structured PDF text into line-level features
    suitable for ML classification.
    """

    def __init__(self, structured_pages: List[Dict]):
        self.structured_pages = structured_pages

    def extract(self) -> List[Dict]:
        """
        Extract line-level features for entire document.
        """

        all_features = []

        for page in self.structured_pages:
            page_number = page["page_number"]

            # Collect all font sizes in page to compute average
            page_font_sizes = []

            for block in page["blocks"]:
                for line in block["lines"]:
                    for span in line:
                        page_font_sizes.append(span["size"])

            if not page_font_sizes:
                continue

            avg_font_size = mean(page_font_sizes)

            for block in page["blocks"]:
                block_bbox = block["bbox"]

                for line in block["lines"]:
                    line_text = " ".join(span["text"] for span in line).strip()

                    if not line_text:
                        continue

                    max_font_size = max(span["size"] for span in line)
                    bold_flag = max(is_bold(span["font"]) for span in line)

                    # Use first span bbox for y-position
                    x0, y0, x1, y1 = line[0]["bbox"]

                    feature_row = {
                        "page_number": page_number,
                        "text": line_text,

                        # --- Typography Features ---
                        "font_size": max_font_size,
                        "font_size_relative": max_font_size / avg_font_size,
                        "is_bold": bold_flag,

                        # --- Text Features ---
                        "uppercase_ratio": uppercase_ratio(line_text),
                        "text_length": text_length(line_text),
                        "contains_numbering": contains_numbering(line_text),

                        # --- Layout Features ---
                        "y_position": y0,
                        "block_x0": block_bbox[0],
                        "block_width": block_bbox[2] - block_bbox[0],

                        # Placeholder for supervised learning
                        "label": None
                    }

                    all_features.append(feature_row)

        return all_features