import pytest
from unittest.mock import patch
from rpa_pdf import Stamp


@pytest.fixture
def stamp():
    return Stamp()


@patch("rpa_pdf.Stamp.BarcodeGenerator.generate_code39_stamp")
def test_generate_code39_stamp(mock_generate, stamp):
    stamp.generate_code39_stamp("12345678", "stamp.pdf", width=80, height=40)
    mock_generate.assert_called_once_with("12345678", "stamp.pdf", width=80, height=40)


@patch("rpa_pdf.Stamp.BarcodeGenerator.generate_code39_stamp")
@patch("rpa_pdf.Stamp.PdfStamper.merge_stamp")
def test_add_code39_stamp(mock_merge, mock_generate, stamp):
    stamp.add_code39_stamp("input.pdf", "out.pdf", "10000000")
    mock_generate.assert_called_once()
    mock_merge.assert_called_once()


@patch("rpa_pdf.Stamp.PdfStamper.add_text_stamp")
def test_add_text_stamp(mock_add_text, stamp):
    stamp.add_text_stamp("input.pdf", "out2.pdf", "dupa")
    mock_add_text.assert_called_once_with("input.pdf", "out2.pdf", "dupa")
