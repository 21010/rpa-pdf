import os
from pypdf import PdfReader, PdfWriter


class PdfSplitter:
    def split(self, pdf_file_path: str, output_directory: str | None = None) -> list[str]:
        if not os.path.exists(pdf_file_path):
            raise FileNotFoundError(f"{pdf_file_path} does not exist")

        if output_directory is None:
            output_directory = os.path.dirname(pdf_file_path)

        reader = PdfReader(pdf_file_path)
        base_name = os.path.splitext(os.path.basename(pdf_file_path))[0]

        output_files = []
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)

            out_path = os.path.join(output_directory, f"{base_name}_page_{i + 1}.pdf")
            with open(out_path, "wb") as f:
                writer.write(f)
            output_files.append(out_path)

        return output_files
