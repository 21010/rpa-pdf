import os
from fpdf import FPDF
from rpa_pdf.converters.base import BaseConverter


class TextConverter(BaseConverter):
    def __init__(self):
        self.__root_dir__: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.__fonts_dir__: str = os.path.join(self.__root_dir__, "fonts")

    def convert(self, input_file_path: str, output_file_path: str | None = None) -> None:
        try:
            with open(input_file_path, "r", encoding="utf-8") as txt_file:
                text_content = txt_file.read()

            pdf = FPDF()
            pdf.add_page()
            pdf.add_font("Dejavu Sans", "", os.path.join(self.__fonts_dir__, "DejaVuSans.ttf"))
            pdf.set_font(family="Dejavu Sans", style="", size=12)
            pdf.multi_cell(0, 10, text=text_content)
            pdf.output(output_file_path)

        except Exception as ex:
            raise ex
