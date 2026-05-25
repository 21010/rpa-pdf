import os
import warnings
from typing import Optional

from .base import BaseConverter
from .image import ImageConverter
from .office import WordConverter, ExcelConverter, PowerPointConverter
from .html import HtmlConverter
from .text import TextConverter
from .email import EmailConverter
from rpa_pdf.common import parse_output_file_path

class Converter:
    def get_converter(self, input_file_path: str) -> Optional[BaseConverter]:
        ext = os.path.splitext(input_file_path)[1].lower()
        match ext:
            case '.doc' | '.docx' | '.rtf':
                return WordConverter()
            case '.xls' | '.xlsx' | '.xlsm' | '.ods' | '.csv':
                return ExcelConverter()
            case '.ppt' | '.pptx' | '.pptm' | '.ppsx':
                return PowerPointConverter()
            case '.png' | '.jpg' | '.jpeg' | '.gif' | '.tiff' | '.bmp' | '.tif':
                return ImageConverter()
            case '.msg' | '.eml':
                return EmailConverter()
            case '.html' | '.htm':
                return HtmlConverter()
            case '.txt':
                return TextConverter()
            case _:
                return None

    def convert(self, input_file_path: str, output_file_path: str | None = None, index: int | None = None) -> bool:
        if not os.path.exists(input_file_path):
            raise FileNotFoundError(f'{input_file_path} does not exist')

        converter = self.get_converter(input_file_path)
        if not converter:
            warnings.warn(f'[Not Implemented] {input_file_path} - cannot convert {os.path.splitext(input_file_path)[1]} file.')
            return False

        out_path = self._get_output_path(input_file_path, output_file_path, index)
        converter.convert(input_file_path, out_path)
        return True

    def _get_output_path(self, input_file_path: str, output_file_path: str | None = None, index: int | None = None) -> str:
        directory, filename = os.path.split(parse_output_file_path(input_file_path, output_file_path))
        filename_parts = os.path.splitext(filename)

        new_filename = f"{filename_parts[0]}{filename_parts[1]}"
        if index is not None:
            new_filename = f"{index}_{new_filename}"

        out_path = os.path.join(directory, new_filename)
        if os.path.exists(out_path):
            os.remove(out_path)
        return out_path
