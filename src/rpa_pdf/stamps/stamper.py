import os
from typing import Literal
import tempfile
from pypdf import PdfReader, PdfWriter
from rpa_pdf.pdf.generator import PdfGenerator


class PdfStamper:
    def __init__(self):
        self._generator = PdfGenerator()

    def merge_stamp(
        self,
        input_pdf_file_path: str,
        output_pdf_file_path: str,
        stamp_pdf_file_path: str,
        apply_for_pages: Literal["all", "first", "last"] | list[int] = "first",
        remove_input_file: bool = False,
        remove_stamp_file: bool = False,
    ) -> None:
        if not os.path.exists(input_pdf_file_path):
            raise FileNotFoundError(f"{input_pdf_file_path} doesn't exist")
        if not os.path.exists(stamp_pdf_file_path):
            raise FileNotFoundError(f"{stamp_pdf_file_path} doesn't exist")

        watermark_reader = PdfReader(stamp_pdf_file_path)
        watermark = watermark_reader.pages[0]

        pdf_document = PdfReader(input_pdf_file_path)

        if not isinstance(apply_for_pages, list):
            match apply_for_pages:
                case "all":
                    apply_for_pages = list(range(0, len(pdf_document.pages)))
                case "last":
                    apply_for_pages = [-1]
                case "first":
                    apply_for_pages = [0]
                case _:
                    raise ValueError("incorrect value of apply_for_pages argument")

        output = PdfWriter()
        for index, page in enumerate(pdf_document.pages):
            output.add_page(page)
            if index in apply_for_pages:
                output.pages[-1].merge_page(watermark)

        output.write(output_pdf_file_path)

        if remove_stamp_file and os.path.exists(stamp_pdf_file_path):
            try:
                os.remove(stamp_pdf_file_path)
            except OSError:
                pass
        if remove_input_file and os.path.exists(input_pdf_file_path):
            try:
                os.remove(input_pdf_file_path)
            except OSError:
                pass

    def add_text_stamp(
        self,
        input_pdf_file_path: str,
        output_pdf_file_path: str,
        text: str,
        *,
        apply_for_pages: Literal["all", "first", "last"] | list[int] = "first",
        remove_input_file: bool = False,
        font_family: str = "DejaVu",
        font_file_path: str | bool = False,
        font_unicode: bool = True,
        font_style: Literal[
            "", "B", "I", "U", "BU", "UB", "BI", "IB", "IU", "UI", "BIU", "BUI", "IBU", "IUB", "UBI", "UIB"
        ] = "",
        font_size: int = 12,
        text_vertical_position: Literal["top", "center", "bottom"] = "top",
        text_horizontal_position: Literal["left", "center", "right"] = "left",
        page_orientation: Literal["portrait", "landscape"] = "portrait",
        page_units: Literal["mm", "pt", "cm", "in"] = "mm",
        page_format: Literal["A3", "A4", "A5", "Letter", "Legal"] | tuple[float, float] = "A4",
        page_vertical_margin: int = 10,
        page_horizontal_margin: int = 10,
    ) -> None:
        if not os.path.exists(input_pdf_file_path):
            raise FileNotFoundError(f"{input_pdf_file_path} doesn't exist")

        watermark_pdf_file_path = os.path.join(tempfile.gettempdir(), "text_stamp.pdf")
        self._generator.text_to_pdf(
            text=text,
            output_file_path=watermark_pdf_file_path,
            font_family=font_family,
            font_file_path=font_file_path,
            font_unicode=font_unicode,
            font_style=font_style,
            font_size=font_size,
            text_vertical_position=text_vertical_position,
            text_horizontal_position=text_horizontal_position,
            page_orientation=page_orientation,
            page_units=page_units,
            page_format=page_format,
            page_vertical_margin=page_vertical_margin,
            page_horizontal_margin=page_horizontal_margin,
        )

        self.merge_stamp(
            input_pdf_file_path=input_pdf_file_path,
            output_pdf_file_path=output_pdf_file_path,
            stamp_pdf_file_path=watermark_pdf_file_path,
            apply_for_pages=apply_for_pages,
            remove_input_file=remove_input_file,
            remove_stamp_file=True,
        )
