import os
from typing import Literal
from pypdf import PdfReader, PdfWriter


class PdfRotator:
    def rotate(
        self,
        pdf_file_path: str,
        angle: Literal[90, 180, 270],
        pages: Literal["all", "first", "last"] | list[int] = "all",
        output_file_path: str | None = None,
    ) -> None:
        if not os.path.exists(pdf_file_path):
            raise FileNotFoundError(f"{pdf_file_path} does not exist")

        if angle not in (90, 180, 270):
            raise ValueError("Angle must be 90, 180, or 270")

        reader = PdfReader(pdf_file_path)
        writer = PdfWriter()

        if not isinstance(pages, list):
            match pages:
                case "all":
                    pages = list(range(len(reader.pages)))
                case "first":
                    pages = [0]
                case "last":
                    pages = [-1]

        total_pages = len(reader.pages)
        pages = [p if p >= 0 else total_pages + p for p in pages]

        for i, page in enumerate(reader.pages):
            if i in pages:
                page.rotate(angle)
            writer.add_page(page)

        out_path = output_file_path or pdf_file_path
        with open(out_path, "wb") as f:
            writer.write(f)
