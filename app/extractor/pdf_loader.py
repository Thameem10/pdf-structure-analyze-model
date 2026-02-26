import fitz  # PyMuPDF
from pathlib import Path

class PDFLoader:
    """
    Handles loading and basic validation of PDF files.
    """

    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        self.document = None

    def validate(self):
        """
        Validate if file exists and is a PDF.
        """
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"File not found: {self.pdf_path}")

        if self.pdf_path.suffix.lower() != ".pdf":
            raise ValueError("Provided file is not a PDF.")

    def load(self):
        """
        Load the PDF document.
        """
        self.validate()

        try:
            self.document = fitz.open(self.pdf_path)
            return self.document
        except Exception as e:
            raise RuntimeError(f"Failed to open PDF: {e}")

    def get_page_count(self):
        """
        Return number of pages in the PDF.
        """
        if not self.document:
            raise ValueError("PDF not loaded. Call load() first.")

        return len(self.document)

    def get_metadata(self):
        """
        Return PDF metadata.
        """
        if not self.document:
            raise ValueError("PDF not loaded. Call load() first.")

        return self.document.metadata

    def close(self):
        """
        Close the PDF document safely.
        """
        if self.document:
            self.document.close()