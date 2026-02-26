import sys
from app.pipeline import PDFPipeline


def main():

    if len(sys.argv) < 2:
        print("Usage: python -m app.main <pdf_path>")
        return

    # Join everything after script name
    pdf_path = " ".join(sys.argv[1:])

    pipeline = PDFPipeline(pdf_path)
    pipeline.run()


if __name__ == "__main__":
    main()