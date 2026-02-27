import camelot
import os

class TableExtractor:
    """
    Extracts tables from PDF using Camelot
    and returns structured layout elements.
    """

    def __init__(self, pdf_path, output_folder="data/output/tables"):
        self.pdf_path = pdf_path
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

    def extract(self):
        """
        Extract tables with bounding boxes and metadata.
        Returns structured table layout elements.
        """

        table_elements = []

        # Extract tables from all pages
        tables = camelot.read_pdf(
            self.pdf_path,
            pages="all",
            flavor="stream"  # use "lattice" if tables have borders
        )

        for idx, table in enumerate(tables):

            # Save table as CSV (optional but useful)
            table_filename = f"table_{idx+1}.csv"
            table_path = os.path.join(self.output_folder, table_filename)
            table.df.to_csv(table_path, index=False)

            # Extract bounding box
            x0, y0, x1, y1 = table._bbox

            width = x1 - x0
            height = y1 - y0
            area = width * height

            page_number = table.page

            table_elements.append({
                "type": "Table",
                "page_number": int(page_number),
                "table_path": table_path,
                "bbox": [x0, y0, x1, y1],
                "width": width,
                "height": height,
                "area": area,
                "aspect_ratio": width / height if height != 0 else 0,
                "rows": table.shape[0],
                "columns": table.shape[1],
                "y_position": float(y0)  # for layout sorting
            })

        return table_elements