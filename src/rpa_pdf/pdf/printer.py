import os
import subprocess  # nosec B404
from typing import Literal
from rpa_pdf.common import EXEC_DIR


class PdfPrinter:
    def print(
        self,
        pdf_file_path: str,
        printer: str = "default",
        pages: Literal["all", "first", "last"] | list[str] = "all",
        odd_or_even: Literal["odd", "even"] | bool = False,
        orientation: Literal["portrait", "landscape"] = "portrait",
        scale: Literal["noscale", "shrink", "fit"] = "fit",
        color: Literal["color", "monochrome"] = "color",
        mode: Literal["duplex", "duplexshort", "simplex"] = "simplex",
        paper: Literal["A2", "A3", "A4", "A5", "A6", "letter", "legal", "tabloid", "statement"] = "A4",
    ) -> None:
        if not os.path.exists(pdf_file_path):
            raise FileNotFoundError(f"{pdf_file_path} does not exist")

        sumatra_path = os.path.join(EXEC_DIR, "sumatra.exe")
        args = [sumatra_path]

        if printer == "default":
            args.append("-print-to-default")
        else:
            args.extend(["-print-to", printer])

        settings = []
        if isinstance(pages, list):
            settings.append(",".join(pages))
        else:
            match pages.lower():
                case "first":
                    settings.append("1")
                case "last":
                    settings.append("-1")
                case "all":
                    settings.append("*")
                case _:
                    raise ValueError("incorrect range of pages")

        if isinstance(odd_or_even, str):
            match odd_or_even.lower():
                case "odd":
                    settings.append("odd")
                case "even":
                    settings.append("even")
                case _:
                    raise ValueError("incorrect odd_or_even")

        settings.append(orientation)
        settings.append(scale)
        settings.append(color)
        settings.append(mode)
        settings.append(f"paper={paper}")

        args.extend(["-print-settings", ",".join(settings), "-silent", pdf_file_path])
        subprocess.run(args, check=True)  # nosec B603
