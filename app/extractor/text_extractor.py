import re
from typing import List, Dict
from statistics import mean
from app.features.feature_utils import is_bold


class TextExtractor:
    """
    Extracts flat text layout elements from PyMuPDF document.
    Each line becomes one 'Text' layout element.
    """

    def __init__(self, document):
        self.document = document

    
    @staticmethod
    def compute_text_features(text: str):
        text = text.strip()
        length = len(text)

        if length == 0:
            return {
                "text_length": 0,
                "uppercase_ratio": 0,
                "digit_ratio": 0,
                "punctuation_ratio": 0,
                "ends_with_period": 0,
                "title_case_ratio": 0,
                "contains_colon": 0,
                "contains_numbering": 0,
                "word_count": 0
            }

        uppercase_ratio = sum(1 for c in text if c.isupper()) / length
        digit_ratio = sum(1 for c in text if c.isdigit()) / length
        punctuation_ratio = sum(1 for c in text if c in ".,;:!?") / length
        ends_with_period = int(text.endswith("."))
        contains_colon = int(":" in text)

        words = text.split()
        word_count = len(words)

        title_case_ratio = sum(1 for w in words if w.istitle()) / word_count if word_count else 0

        # FIXED REGEX
        contains_numbering = int(bool(re.match(r"^\d+(\.|\))", text)))

        return {
            "text_length": length,
            "uppercase_ratio": uppercase_ratio,
            "digit_ratio": digit_ratio,
            "punctuation_ratio": punctuation_ratio,
            "ends_with_period": ends_with_period,
            "title_case_ratio": title_case_ratio,
            "contains_colon": contains_colon,
            "contains_numbering": contains_numbering,
            "word_count": word_count
        }
    
    def extract(self) -> List[Dict]:

        text_elements = []

        for page_number, page in enumerate(self.document):

            page_dict = page.get_text("dict")

            # Collect all font sizes to compute page average
            page_font_sizes = []

            for block in page_dict["blocks"]:
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        page_font_sizes.append(span["size"])

            if not page_font_sizes:
                continue

            avg_font_size = mean(page_font_sizes)

            for block in page_dict["blocks"]:

                if "lines" not in block:
                    continue

                block_bbox = block["bbox"]

                for line in block["lines"]:

                    spans = line["spans"]

                    line_text = " ".join(
                        span["text"].strip() for span in spans if span["text"].strip()
                    ).strip()

                    if not line_text:
                        continue

                    max_font_size = max(span["size"] for span in spans)
                    bold_flag = max(is_bold(span["font"]) for span in spans)

                    # Use first span bbox for y-position
                    x0, y0, x1, y1 = spans[0]["bbox"]
                    
                    text_features = TextExtractor.compute_text_features(line_text)

                    text_elements.append({
                        "type": "Text",
                        "page_number": page_number + 1,
                        "content": line_text,

                        # Typography
                        "font_size": max_font_size,
                        "font_size_relative": max_font_size / avg_font_size,
                        "is_bold": bold_flag,

                        # Layout
                        "y_position": y0,
                        "block_width": block_bbox[2] - block_bbox[0],
                        "bbox": [x0, y0, x1, y1],
                        
                        # New Features
                        **text_features
                    })

        return text_elements