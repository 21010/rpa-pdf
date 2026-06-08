from .compressor import PdfCompressor
from .generator import PdfGenerator
from .merger import PdfMerger
from .printer import PdfPrinter
from .splitter import PdfSplitter
from .rotator import PdfRotator
from .extractor import TextExtractor, ImageExtractor

__all__ = [
    "PdfCompressor",
    "PdfGenerator",
    "PdfMerger",
    "PdfPrinter",
    "PdfSplitter",
    "PdfRotator",
    "TextExtractor",
    "ImageExtractor",
    "Pdf",
]


class Pdf:
    def __init__(self):
        self._compressor = PdfCompressor()
        self._generator = PdfGenerator()
        self._merger = PdfMerger()
        self._printer = PdfPrinter()

    def compress(self, pdf_file_path: str) -> None:
        self._compressor.compress(pdf_file_path)

    def text_to_pdf(self, *args, **kwargs) -> None:
        self._generator.text_to_pdf(*args, **kwargs)

    def merge(self, *args, **kwargs) -> None:
        self._merger.merge(*args, **kwargs)

    def print(self, *args, **kwargs) -> None:
        self._printer.print(*args, **kwargs)
