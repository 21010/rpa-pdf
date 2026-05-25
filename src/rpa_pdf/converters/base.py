from abc import ABC, abstractmethod
import os

class BaseConverter(ABC):
    @abstractmethod
    def convert(self, input_file_path: str, output_file_path: str | None = None) -> None:
        pass

    def _get_output_path(self, input_file_path: str, output_file_path: str | None = None, index: int | None = None) -> str:
        from rpa_pdf.common import parse_output_file_path
        directory, filename = os.path.split(parse_output_file_path(input_file_path, output_file_path))
        filename_parts = os.path.splitext(filename)

        new_filename = f"{filename_parts[0]}{filename_parts[1]}"
        if index is not None:
            new_filename = f"{index}_{new_filename}"

        out_path = os.path.join(directory, new_filename)
        if os.path.exists(out_path):
            os.remove(out_path)
        return out_path
