import pytest
from unittest.mock import patch, MagicMock
from PIL import Image
from rpa_pdf import Converter


@pytest.fixture
def converter():
    return Converter()


def test_image_to_pdf(converter, tmp_path):
    input_file = tmp_path / "input.png"
    Image.new("RGB", (10, 10)).save(input_file)

    out_file = tmp_path / "output.pdf"
    assert converter.convert(str(input_file), str(out_file)) is True
    assert out_file.exists()


@patch("comtypes.client.CreateObject")
def test_word_to_pdf(mock_create_object, converter, tmp_path):
    mock_word = MagicMock()
    mock_create_object.return_value = mock_word

    input_file = tmp_path / "input.docx"
    input_file.touch()

    out_file = tmp_path / "output.pdf"
    assert converter.convert(str(input_file), str(out_file)) is True
    mock_word.Documents.Open.assert_called_once()
    mock_word.Documents.Open.return_value.SaveAs.assert_called_once_with(str(out_file), FileFormat=17)


@patch("comtypes.client.CreateObject")
def test_excel_to_pdf(mock_create_object, converter, tmp_path):
    mock_excel = MagicMock()
    mock_create_object.return_value = mock_excel
    mock_sheet = MagicMock()
    mock_excel.Workbooks.Open.return_value.Worksheets = [mock_sheet]

    input_file = tmp_path / "input.xlsx"
    input_file.touch()

    out_file = tmp_path / "output.pdf"
    assert converter.convert(str(input_file), str(out_file)) is True
    mock_excel.Workbooks.Open.assert_called_once()


@patch("comtypes.client.CreateObject")
def test_powerpoint_to_pdf(mock_create_object, converter, tmp_path):
    mock_ppt = MagicMock()
    mock_create_object.return_value = mock_ppt

    input_file = tmp_path / "input.pptx"
    input_file.touch()

    out_file = tmp_path / "output.pdf"
    assert converter.convert(str(input_file), str(out_file)) is True
    mock_ppt.Presentations.Open.assert_called_once()


def test_html_to_pdf(converter, tmp_path):
    input_file = tmp_path / "input.html"
    input_file.write_text("<html><body><h1>Test</h1></body></html>", encoding="utf-8")

    out_file = tmp_path / "output.pdf"
    assert converter.convert(str(input_file), str(out_file)) is True
    assert out_file.exists()


def test_txt_to_pdf(converter, tmp_path):
    input_file = tmp_path / "input.txt"
    input_file.write_text("Hello World", encoding="utf-8")

    out_file = tmp_path / "output.pdf"
    assert converter.convert(str(input_file), str(out_file)) is True
    assert out_file.exists()


def test_eml_to_pdf(converter, tmp_path):
    input_file = tmp_path / "input.eml"
    input_file.write_bytes(b"From: test@test.com\nTo: test2@test.com\nSubject: Test\n\nHello\n")

    out_file = tmp_path / "output.pdf"
    assert converter.convert(str(input_file), str(out_file)) is True
    assert out_file.exists()
