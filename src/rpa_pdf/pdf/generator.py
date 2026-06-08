from typing import Literal
from fpdf import FPDF
from rpa_pdf.common import set_x_pos, set_y_pos, FONTS_DIR


class PdfGenerator:
    def text_to_pdf(
        self,
        text: str,
        output_file_path: str,
        font_family: str = "DejaVu Sans",
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
        fpdf = FPDF(orientation=page_orientation, unit=page_units, format=page_format)
        fpdf.compress = True

        font_path = font_file_path if isinstance(font_file_path, str) else f"{FONTS_DIR}\\DejaVuSans.ttf"
        fpdf.add_font(font_family, "", font_path)
        fpdf.set_font(family=font_family, style=font_style, size=font_size)

        fpdf.add_page()
        string_width = fpdf.get_string_width(text)
        x_pos = set_x_pos(text_horizontal_position, page_horizontal_margin, fpdf.w, string_width)
        y_pos = set_y_pos(text_vertical_position, page_vertical_margin, fpdf.h, font_size)

        fpdf.text(x_pos, y_pos, text)
        fpdf.output(output_file_path)
