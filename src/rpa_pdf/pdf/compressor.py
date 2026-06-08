import os
from pypdf import PdfReader, PdfWriter


class PdfCompressor:
    def compress(self, pdf_file_path: str) -> None:
        if not os.path.exists(pdf_file_path):
            raise FileNotFoundError(f"{pdf_file_path} does not exist")

        writer = PdfWriter()
        reader = PdfReader(pdf_file_path)
        writer.clone_document_from_reader(reader)
        for page in writer.pages:
            page.compress_content_streams()
        with open(pdf_file_path, "wb") as pdf:
            writer.write(pdf)
