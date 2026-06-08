from unittest.mock import patch, MagicMock
import pytest
from rpa_pdf.pdf.extractor import TextExtractor, ImageExtractor


@patch("os.path.exists", return_value=True)
@patch("rpa_pdf.pdf.extractor.PdfReader")
def test_extract_text_all_pages(mock_reader, mock_exists):
    mock_pdf = MagicMock()
    mock_page1 = MagicMock()
    mock_page1.extract_text.return_value = "Page 1 Text"
    mock_page2 = MagicMock()
    mock_page2.extract_text.return_value = "Page 2 Text"
    mock_pdf.pages = [mock_page1, mock_page2]
    mock_reader.return_value = mock_pdf

    extractor = TextExtractor()
    result = extractor.extract_text("dummy.pdf")

    assert "Page 1 Text\nPage 2 Text" == result


@patch("os.path.exists", return_value=True)
@patch("rpa_pdf.pdf.extractor.PdfReader")
def test_extract_text_specific_pages(mock_reader, mock_exists):
    mock_pdf = MagicMock()
    mock_page1 = MagicMock()
    mock_page1.extract_text.return_value = "Page 1 Text"
    mock_page2 = MagicMock()
    mock_page2.extract_text.return_value = "Page 2 Text"
    mock_pdf.pages = [mock_page1, mock_page2]
    mock_reader.return_value = mock_pdf

    extractor = TextExtractor()
    result = extractor.extract_text("dummy.pdf", pages=[1])

    assert "Page 2 Text" == result


@patch("os.path.exists", return_value=False)
def test_extract_text_file_not_found(mock_exists):
    extractor = TextExtractor()
    with pytest.raises(FileNotFoundError):
        extractor.extract_text("missing.pdf")


@patch("os.path.exists", side_effect=lambda x: True if "pdf" in x else False)
@patch("os.makedirs")
@patch("builtins.open")
@patch("rpa_pdf.pdf.extractor.PdfReader")
def test_extract_images(mock_reader, mock_open, mock_makedirs, mock_exists):
    mock_pdf = MagicMock()
    mock_page1 = MagicMock()
    mock_img1 = MagicMock()
    mock_img1.name = "img1.png"
    mock_img1.data = b"image_data"
    mock_page1.images = [mock_img1]
    mock_pdf.pages = [mock_page1]
    mock_reader.return_value = mock_pdf

    extractor = ImageExtractor()
    result = extractor.extract_images("dummy.pdf", "output_dir")

    assert len(result) == 1
    assert "img1.png" in result[0]
    mock_makedirs.assert_called_once()
    mock_open.assert_called_once()


@patch("os.path.exists", return_value=False)
def test_extract_images_file_not_found(mock_exists):
    extractor = ImageExtractor()
    with pytest.raises(FileNotFoundError):
        extractor.extract_images("missing.pdf", "output_dir")
