import json
from app.extractor.pdf_loader import PDFLoader
from app.extractor.text_extractor import TextExtractor
from app.extractor.image_extractor import ImageExtractor
from app.extractor.table_extractor import TableExtractor
from app.features.feature_extractor import FeatureExtractor
import warnings
warnings.filterwarnings("ignore")


class PDFPipeline:
    """
    End-to-end PDF processing pipeline.
    """

    def __init__(self, pdf_path, output_path="data/interim/features.json"):
        self.pdf_path = pdf_path
        self.output_path = output_path

    def run(self):

        # Load PDF
        loader = PDFLoader(self.pdf_path)
        document = loader.load()

        # Extract text
        text_extractor = TextExtractor(document)
        text_elements = text_extractor.extract()

        # Extract images 
        image_extractor = ImageExtractor(document)
        image_elements = image_extractor.extract()
        
        # Extract tables 
        table_extractor = TableExtractor(self.pdf_path)
        table_elements = table_extractor.extract()

        all_elements = text_elements + image_elements + table_elements

        # Normalize layout keys
        for element in all_elements:
            element.setdefault("page_number", 0)
            element.setdefault("y_position", 0)

        # Sort by page and vertical position
        all_elements.sort(
            key=lambda x: (x["page_number"], x["y_position"])
        )
        
        # Extract features
        feature_extractor = FeatureExtractor(all_elements)
        features = feature_extractor.extract()

        loader.close()

        # Save features
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(features, f, indent=4, ensure_ascii=False)

        print(f"Feature extraction complete. Saved to {self.output_path}")

        return features