import json
from app.extractor.pdf_loader import PDFLoader
from app.extractor.text_extractor import TextExtractor
from app.extractor.image_extractor import ImageExtractor
from app.features.feature_extractor import FeatureExtractor


class PDFPipeline:
    """
    End-to-end PDF processing pipeline.
    """

    def __init__(self, pdf_path, output_path="data/interim/features.json"):
        self.pdf_path = pdf_path
        self.output_path = output_path

    def run(self):

        # 1️⃣ Load PDF
        loader = PDFLoader(self.pdf_path)
        document = loader.load()

        # 2️⃣ Extract text
        text_extractor = TextExtractor(document)
        structured_pages = text_extractor.extract()

        # 3️⃣ Extract images (optional for ML now)
        image_extractor = ImageExtractor(document)
        image_extractor.extract()

        # 4️⃣ Extract features
        feature_extractor = FeatureExtractor(structured_pages)
        features = feature_extractor.extract()

        loader.close()

        # 5️⃣ Save features
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(features, f, indent=4, ensure_ascii=False)

        print(f"Feature extraction complete. Saved to {self.output_path}")

        return features