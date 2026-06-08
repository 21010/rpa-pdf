import os
import tempfile
from typing import Literal
from .stamps.barcode import BarcodeGenerator
from .stamps.stamper import PdfStamper


class Stamp:
    """Stamp class - Facade for BarcodeGenerator and PdfStamper"""

    def __init__(self) -> None:
        self.__root_dir__: str = os.path.dirname(os.path.abspath(__file__))
        self.__fonts_dir__: str = os.path.join(self.__root_dir__, "fonts")
        self.__exec_dir__: str = os.path.join(self.__root_dir__, "exec")

        self._barcode_generator = BarcodeGenerator()
        self._stamper = PdfStamper()

    def generate_code39_stamp(self, *args, **kwargs) -> None:
        self._barcode_generator.generate_code39_stamp(*args, **kwargs)

    def add_code39_stamp(
        self,
        input_pdf_file_path: str,
        output_pdf_file_path: str,
        code: str,
        width: float = 40.0,
        height: float = 20.0,
        apply_for_pages: Literal["all", "first", "last"] | list[int] = "first",
        remove_input_file: bool = False,
        vertical_position: Literal["top", "center", "bottom"] = "top",
        horizontal_position: Literal["left", "center", "right"] = "left",
        page_orientation: Literal["portrait", "landscape"] = "portrait",
        page_units: Literal["mm", "pt", "cm", "in"] = "mm",
        page_format: Literal["A3", "A4", "A5", "Letter", "Legal"] | tuple[float, float] = "A4",
        page_vertical_margin: int = 0,
        page_horizontal_margin: int = 0,
    ) -> None:
        stamp_path = os.path.join(tempfile.gettempdir(), "barcode_stamp.pdf")
        self._barcode_generator.generate_code39_stamp(
            code=code,
            output_file_path=stamp_path,
            output_file_format="pdf",
            width=width,
            height=height,
            vertical_position=vertical_position,
            horizontal_position=horizontal_position,
            page_orientation=page_orientation,
            page_units=page_units,
            page_format=page_format,
            page_vertical_margin=page_vertical_margin,
            page_horizontal_margin=page_horizontal_margin,
        )
        self._stamper.merge_stamp(
            input_pdf_file_path=input_pdf_file_path,
            output_pdf_file_path=output_pdf_file_path,
            stamp_pdf_file_path=stamp_path,
            apply_for_pages=apply_for_pages,
            remove_input_file=remove_input_file,
            remove_stamp_file=True,
        )

    def add_text_stamp(self, *args, **kwargs) -> None:
        self._stamper.add_text_stamp(*args, **kwargs)
