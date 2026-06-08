import pytest
from unittest.mock import patch, MagicMock
from rpa_pdf import Pdf


@pytest.fixture
def pdf():
    return Pdf()


@patch("os.path.exists", return_value=True)
@patch("builtins.open")
@patch("rpa_pdf.pdf.compressor.PdfWriter")
@patch("rpa_pdf.pdf.compressor.PdfReader")
def test_compress(mock_reader, mock_writer, mock_open, mock_exists, pdf):
    # Mocking PdfReader to have some dummy pages
    mock_pdf_instance = MagicMock()
    mock_page = MagicMock()
    mock_pdf_instance.pages = [mock_page]
    mock_reader.return_value = mock_pdf_instance

    mock_writer_instance = MagicMock()
    mock_writer_instance.pages = [mock_page]
    mock_writer.return_value = mock_writer_instance

    pdf.compress("input.pdf")

    mock_reader.assert_called_once_with("input.pdf")
    mock_page.compress_content_streams.assert_called_once()
    mock_writer_instance.clone_document_from_reader.assert_called_once()
    mock_writer_instance.write.assert_called_once()


@patch("rpa_pdf.pdf.generator.FPDF")
def test_text_to_pdf(mock_fpdf, pdf):
    mock_fpdf_instance = MagicMock()
    mock_fpdf.return_value = mock_fpdf_instance

    pdf.text_to_pdf("hello", "output.pdf")

    mock_fpdf_instance.add_page.assert_called_once()
    mock_fpdf_instance.text.assert_called_once()
    mock_fpdf_instance.output.assert_called_once_with("output.pdf")


@patch("os.path.exists", return_value=True)
@patch("rpa_pdf.pdf.merger.PdfWriter")
@patch("rpa_pdf.pdf.merger.PdfReader")
def test_merge(mock_reader, mock_writer, mock_exists, pdf):
    mock_writer_instance = MagicMock()
    mock_writer.return_value = mock_writer_instance

    mock_reader_instance = MagicMock()
    mock_reader.return_value = mock_reader_instance

    pdf.merge(["file1.pdf", "file2.pdf"], "merged.pdf")

    assert mock_reader.call_count == 2
    assert mock_writer_instance.append.call_count == 2
    mock_writer_instance.write.assert_called_once_with("merged.pdf")


@patch("os.path.exists", return_value=True)
@patch("subprocess.run")
def test_print(mock_run, mock_exists, pdf):
    pdf.print("sample.pdf", printer="Bullzip PDF Printer")
    mock_run.assert_called_once()
