import tempfile
import extract_msg
import email
from email import policy
from rpa_pdf.converters.base import BaseConverter
from rpa_pdf.converters.html import HtmlConverter


class EmailConverter(BaseConverter):
    def convert(self, input_file_path: str, output_file_path: str | None = None) -> None:
        try:
            html_content = ""
            if input_file_path.lower().endswith(".msg"):
                msg = extract_msg.Message(input_file_path)
                html_content = msg.htmlBody
                if not html_content:
                    html_content = f"<pre>{msg.body}</pre>" if msg.body else ""

                if isinstance(html_content, bytes):
                    html_content = html_content.decode("utf-8", errors="ignore")
            else:
                with open(input_file_path, "rb") as f:
                    msg = email.message_from_binary_file(f, policy=policy.default)
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/html":
                                html_content = part.get_content()
                                break
                            elif part.get_content_type() == "text/plain":
                                html_content = f"<pre>{part.get_content()}</pre>"
                    else:
                        if msg.get_content_type() == "text/html":
                            html_content = msg.get_content()
                        else:
                            html_content = f"<pre>{msg.get_content()}</pre>"

            with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as f:
                f.write(html_content)
                temp_html = f.name

            try:
                html_converter = HtmlConverter()
                html_converter.convert(temp_html, output_file_path)
            finally:
                import os

                if os.path.exists(temp_html):
                    os.remove(temp_html)

        except Exception as ex:
            raise ex
