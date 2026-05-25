from xhtml2pdf import pisa
from rpa_pdf.converters.base import BaseConverter


class HtmlConverter(BaseConverter):
    def convert(self, input_file_path: str, output_file_path: str | None = None) -> None:
        try:
            if output_file_path is None:
                raise ValueError("output_file_path must be provided")
            with open(input_file_path, "r", encoding="utf-8") as source_html:
                with open(output_file_path, "wb") as result_file:
                    pisa_status = pisa.CreatePDF(source_html.read(), dest=result_file)
            if pisa_status.err:
                raise Exception("HTML to PDF conversion failed")
        except Exception as ex:
            raise ex
