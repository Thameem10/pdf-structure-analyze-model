from typing import List, Dict


class TextExtractor:
    """
    Extracts structured text (blocks, lines, spans)
    from a PyMuPDF document.
    """

    def __init__(self, document):
        self.document = document

    def extract(self) -> List[Dict]:
        """
        Returns structured text per page.
        """

        extracted_pages = []

        for page_number, page in enumerate(self.document):

            page_data = {
                "page_number": page_number + 1,
                "blocks": []
            }

            page_dict = page.get_text("dict")

            for block in page_dict["blocks"]:
                if "lines" not in block:
                    continue  # skip non-text blocks

                block_data = {
                    "bbox": block["bbox"],
                    "lines": []
                }

                for line in block["lines"]:
                    line_data = []

                    for span in line["spans"]:
                        span_data = {
                            "text": span["text"].strip(),
                            "font": span["font"],
                            "size": span["size"],
                            "bbox": span["bbox"]
                        }

                        if span_data["text"]:
                            line_data.append(span_data)

                    if line_data:
                        block_data["lines"].append(line_data)

                if block_data["lines"]:
                    page_data["blocks"].append(block_data)

            extracted_pages.append(page_data)

        return extracted_pages