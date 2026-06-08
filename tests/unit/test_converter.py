import pytest
from unittest.mock import patch
from rpa_pdf import Converter


@pytest.fixture
def converter():
    return Converter()


@patch("os.path.exists", return_value=True)
@patch("os.remove")
@patch("rpa_pdf.converters.image.ImageConverter.convert")
def test_image_to_pdf(mock_image_convert, mock_remove, mock_exists, converter):
    input_file = "input.png"
    out_file = "output.pdf"
    assert converter.convert(input_file, out_file) is True
    mock_image_convert.assert_called_once()


@patch("os.path.exists", return_value=True)
@patch("os.remove")
@patch("rpa_pdf.converters.office.WordConverter.convert")
def test_word_to_pdf(mock_word_convert, mock_remove, mock_exists, converter):
    input_file = "input.docx"
    out_file = "output.pdf"
    assert converter.convert(input_file, out_file) is True
    mock_word_convert.assert_called_once()


@patch("os.path.exists", return_value=True)
@patch("os.remove")
@patch("rpa_pdf.converters.office.ExcelConverter.convert")
def test_excel_to_pdf(mock_excel_convert, mock_remove, mock_exists, converter):
    input_file = "input.xlsx"
    out_file = "output.pdf"
    assert converter.convert(input_file, out_file) is True
    mock_excel_convert.assert_called_once()


@patch("os.path.exists", return_value=True)
@patch("os.remove")
@patch("rpa_pdf.converters.office.PowerPointConverter.convert")
def test_powerpoint_to_pdf(mock_ppt_convert, mock_remove, mock_exists, converter):
    input_file = "input.pptx"
    out_file = "output.pdf"
    assert converter.convert(input_file, out_file) is True
    mock_ppt_convert.assert_called_once()


@patch("os.path.exists", return_value=True)
@patch("os.remove")
@patch("rpa_pdf.converters.html.HtmlConverter.convert")
def test_html_to_pdf(mock_html_convert, mock_remove, mock_exists, converter):
    input_file = "input.html"
    out_file = "output.pdf"
    assert converter.convert(input_file, out_file) is True
    mock_html_convert.assert_called_once()


@patch("os.path.exists", return_value=True)
@patch("os.remove")
@patch("rpa_pdf.converters.text.TextConverter.convert")
def test_txt_to_pdf(mock_txt_convert, mock_remove, mock_exists, converter):
    input_file = "input.txt"
    out_file = "output.pdf"
    assert converter.convert(input_file, out_file) is True
    mock_txt_convert.assert_called_once()


@patch("os.path.exists", return_value=True)
@patch("os.remove")
@patch("rpa_pdf.converters.email.EmailConverter.convert")
def test_eml_to_pdf(mock_eml_convert, mock_remove, mock_exists, converter):
    input_file = "input.eml"
    out_file = "output.pdf"
    assert converter.convert(input_file, out_file) is True
    mock_eml_convert.assert_called_once()
