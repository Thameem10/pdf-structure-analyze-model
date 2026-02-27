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

    def is_empty_table(self, table):
        """
        Check if table is empty or meaningless.
        """

        # No rows or columns
        if table.shape[0] == 0 or table.shape[1] == 0:
            return True

        df = table.df

        # All cells empty or whitespace
        if df.applymap(lambda x: str(x).strip() == "").all().all():
            return True

        # Very tiny tables (optional filter)
        x0, y0, x1, y1 = table._bbox
        width = x1 - x0
        height = y1 - y0
        area = width * height

        if area < 1000:  # adjust threshold if needed
            return True

        return False

    def extract(self):

        table_elements = []

        tables = camelot.read_pdf(
            self.pdf_path,
            pages="all",
            flavor="lattice"
        )

        for idx, table in enumerate(tables):

            # Skip empty tables
            if self.is_empty_table(table):
                continue

            # Save valid table
            table_filename = f"table_{idx+1}.csv"
            table_path = os.path.join(self.output_folder, table_filename)
            table.df.to_csv(table_path, index=False)

            x0, y0, x1, y1 = table._bbox

            width = x1 - x0
            height = y1 - y0
            area = width * height

            page_number = table.page

            table_elements.append({
                "type": "Table",
                "content": table_filename,
                "page_number": int(page_number),
                "table_path": table_path,
                "bbox": [x0, y0, x1, y1],
                "width": width,
                "height": height,
                "area": area,
                "aspect_ratio": width / height if height != 0 else 0,
                "rows": table.shape[0],
                "columns": table.shape[1],
                "y_position": float(y0)
            })

        return table_elements