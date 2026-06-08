import os
from pypdf import PdfReader, PdfWriter


class PdfMerger:
    def merge(self, pdf_files: list[str], output_pdf_file_path: str) -> None:
        for file_path in pdf_files:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"{file_path} does not exist")

        merge_file = PdfWriter()
        for pdf_file in pdf_files:
            pdf_reader = PdfReader(pdf_file)
            merge_file.append(pdf_reader)

        merge_file.write(output_pdf_file_path)
        merge_file.close()

        if not os.path.exists(output_pdf_file_path):
            raise FileExistsError(f"{output_pdf_file_path} was not generated.")
