import os

class ImageExtractor:
    """
    Extracts and saves images from PDF.
    """

    def __init__(self, document, output_folder="data/output/images"):
        self.document = document
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

    def extract(self):
        """
        Extract images page-wise.
        """

        image_results = []

        for page_number, page in enumerate(self.document):
            image_list = page.get_images(full=True)

            page_images = []

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = self.document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                image_filename = (
                    f"page{page_number+1}_img{img_index+1}.{image_ext}"
                )

                image_path = os.path.join(self.output_folder, image_filename)

                with open(image_path, "wb") as f:
                    f.write(image_bytes)

                page_images.append(image_path)

            image_results.append({
                "page_number": page_number + 1,
                "images": page_images
            })

        return image_results