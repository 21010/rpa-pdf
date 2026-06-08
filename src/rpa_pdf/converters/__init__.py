import os
import warnings
from typing import Optional, Type

from .base import BaseConverter
from .image import ImageConverter
from .office import WordConverter, ExcelConverter, PowerPointConverter
from .html import HtmlConverter
from .text import TextConverter
from .email import EmailConverter
from rpa_pdf.common import parse_output_file_path

# Converter Registry mapping extensions to Converter classes
_CONVERTER_REGISTRY: dict[str, Type[BaseConverter]] = {
    ".doc": WordConverter,
    ".docx": WordConverter,
    ".rtf": WordConverter,
    ".xls": ExcelConverter,
    ".xlsx": ExcelConverter,
    ".xlsm": ExcelConverter,
    ".ods": ExcelConverter,
    ".csv": ExcelConverter,
    ".ppt": PowerPointConverter,
    ".pptx": PowerPointConverter,
    ".pptm": PowerPointConverter,
    ".ppsx": PowerPointConverter,
    ".png": ImageConverter,
    ".jpg": ImageConverter,
    ".jpeg": ImageConverter,
    ".gif": ImageConverter,
    ".tiff": ImageConverter,
    ".bmp": ImageConverter,
    ".tif": ImageConverter,
    ".msg": EmailConverter,
    ".eml": EmailConverter,
    ".html": HtmlConverter,
    ".htm": HtmlConverter,
    ".txt": TextConverter,
}


class Converter:
    @classmethod
    def register_converter(cls, ext: str, converter_class: Type[BaseConverter]) -> None:
        """Registers a new converter class for a specific file extension (e.g., '.pdf')."""
        _CONVERTER_REGISTRY[ext.lower()] = converter_class

    def get_converter(self, input_file_path: str) -> Optional[BaseConverter]:
        ext = os.path.splitext(input_file_path)[1].lower()
        converter_class = _CONVERTER_REGISTRY.get(ext)
        if converter_class:
            return converter_class()
        return None

    def convert(self, input_file_path: str, output_file_path: str | None = None, index: int | None = None) -> bool:
        if not os.path.exists(input_file_path):
            raise FileNotFoundError(f"{input_file_path} does not exist")

        converter = self.get_converter(input_file_path)
        if not converter:
            warnings.warn(
                f"[Not Implemented] {input_file_path} - cannot convert {os.path.splitext(input_file_path)[1]} file."
            )
            return False

        out_path = self._get_output_path(input_file_path, output_file_path, index)
        converter.convert(input_file_path, out_path)
        return True

    def _get_output_path(
        self, input_file_path: str, output_file_path: str | None = None, index: int | None = None
    ) -> str:
        directory, filename = os.path.split(parse_output_file_path(input_file_path, output_file_path))
        filename_parts = os.path.splitext(filename)

        new_filename = f"{filename_parts[0]}{filename_parts[1]}"
        if index is not None:
            new_filename = f"{index}_{new_filename}"

        out_path = os.path.join(directory, new_filename)
        if os.path.exists(out_path):
            os.remove(out_path)
        return out_path
