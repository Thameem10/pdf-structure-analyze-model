import os

class ImageExtractor:
    """
    Extracts images from PDF and returns structured layout elements
    including bounding boxes and metadata.
    """

    def __init__(self, document, output_folder="data/output/images"):
        self.document = document
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

    def extract(self):
        """
        Extract images page-wise with bounding box and metadata.
        Returns structured image layout elements.
        """

        image_elements = []

        for page_number, page in enumerate(self.document):
            image_list = page.get_images(full=True)

            for img_index, img in enumerate(image_list):

                xref = img[0]

                # Extract image bytes
                base_image = self.document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                image_filename = f"page{page_number+1}_img{img_index+1}.{image_ext}"
                image_path = os.path.join(self.output_folder, image_filename)

                # Save image
                with open(image_path, "wb") as f:
                    f.write(image_bytes)

                # Get image bounding box on page
                bbox = page.get_image_bbox(img)

                x0, y0, x1, y1 = bbox

                width = x1 - x0
                height = y1 - y0
                area = width * height

                image_elements.append({
                    "type": "Image",
                    "page_number": page_number + 1,
                    "image_path": image_path,
                    "bbox": [x0, y0, x1, y1],
                    "width": width,
                    "height": height,
                    "area": area,
                    "aspect_ratio": width / height if height != 0 else 0,
                    "y_position": y0  # useful for sorting layout order
                })

        return image_elements