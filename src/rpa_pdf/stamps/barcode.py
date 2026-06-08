import os
import tempfile
from typing import Literal
from fpdf import FPDF
from barcode import Code39
from barcode.writer import ImageWriter
from rpa_pdf.common import set_x_pos, set_y_pos


class BarcodeGenerator:
    def generate_code39_stamp(
        self,
        code: str,
        output_file_path: str,
        output_file_format: Literal["pdf", "png"] = "pdf",
        width: float = 40.0,
        height: float = 20.0,
        vertical_position: Literal["top", "center", "bottom"] = "top",
        horizontal_position: Literal["left", "center", "right"] = "left",
        page_orientation: Literal["portrait", "landscape"] = "portrait",
        page_units: Literal["mm", "pt", "cm", "in"] = "mm",
        page_format: Literal["A3", "A4", "A5", "Letter", "Legal"] | tuple[float, float] = "A4",
        page_vertical_margin: int = 0,
        page_horizontal_margin: int = 0,
    ) -> None:
        barcode_image_path: str = (
            os.path.join(tempfile.gettempdir(), "barcode.png") if output_file_format == "pdf" else output_file_path
        )
        with open(barcode_image_path, "wb") as f:
            Code39(code=code, writer=ImageWriter(), add_checksum=False).write(f)  # type: ignore

        if output_file_format == "png":
            return

        fpdf: FPDF = FPDF(orientation=page_orientation, unit=page_units, format=page_format)
        fpdf.compress = False
        fpdf.add_page()
        fpdf.image(
            name=barcode_image_path,
            x=set_x_pos(horizontal_position, page_horizontal_margin, fpdf.w, width),
            y=set_y_pos(vertical_position, page_vertical_margin, fpdf.h, height),
            w=width,
            h=height,
        )
        fpdf.output(output_file_path)

        if os.path.exists(barcode_image_path) and output_file_format == "pdf":
            try:
                os.remove(barcode_image_path)
            except OSError:
                pass
