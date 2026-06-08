import os
from pypdf import PdfReader


class TextExtractor:
    def extract_text(self, pdf_file_path: str, pages: list[int] | None = None) -> str:
        if not os.path.exists(pdf_file_path):
            raise FileNotFoundError(f"{pdf_file_path} does not exist")

        reader = PdfReader(pdf_file_path)
        extracted_text = []

        target_pages = pages if pages is not None else range(len(reader.pages))

        for i in target_pages:
            if 0 <= i < len(reader.pages):
                text = reader.pages[i].extract_text()
                if text:
                    extracted_text.append(text)

        return "\n".join(extracted_text)


class ImageExtractor:
    def extract_images(self, pdf_file_path: str, output_directory: str) -> list[str]:
        if not os.path.exists(pdf_file_path):
            raise FileNotFoundError(f"{pdf_file_path} does not exist")

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        reader = PdfReader(pdf_file_path)
        saved_images = []

        for i, page in enumerate(reader.pages):
            for count, image_file_object in enumerate(page.images):
                out_path = os.path.join(output_directory, f"page_{i + 1}_img_{count}_{image_file_object.name}")
                with open(out_path, "wb") as fp:
                    fp.write(image_file_object.data)
                saved_images.append(out_path)

        return saved_images
