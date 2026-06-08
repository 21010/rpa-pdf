from unittest.mock import patch, MagicMock
import pytest
from rpa_pdf.pdf.rotator import PdfRotator


@patch("os.path.exists", return_value=True)
@patch("builtins.open")
@patch("rpa_pdf.pdf.rotator.PdfReader")
@patch("rpa_pdf.pdf.rotator.PdfWriter")
def test_rotate_all_pages(mock_writer, mock_reader, mock_open, mock_exists):
    mock_pdf = MagicMock()
    mock_page1 = MagicMock()
    mock_page2 = MagicMock()
    mock_pdf.pages = [mock_page1, mock_page2]
    mock_reader.return_value = mock_pdf

    mock_writer_instance = MagicMock()
    mock_writer.return_value = mock_writer_instance

    rotator = PdfRotator()
    rotator.rotate("dummy.pdf", 90)

    mock_page1.rotate.assert_called_once_with(90)
    mock_page2.rotate.assert_called_once_with(90)
    mock_writer_instance.write.assert_called_once()


@patch("os.path.exists", return_value=True)
@patch("builtins.open")
@patch("rpa_pdf.pdf.rotator.PdfReader")
@patch("rpa_pdf.pdf.rotator.PdfWriter")
def test_rotate_specific_pages(mock_writer, mock_reader, mock_open, mock_exists):
    mock_pdf = MagicMock()
    mock_page1 = MagicMock()
    mock_page2 = MagicMock()
    mock_pdf.pages = [mock_page1, mock_page2]
    mock_reader.return_value = mock_pdf

    rotator = PdfRotator()
    rotator.rotate("dummy.pdf", 180, pages="first")

    mock_page1.rotate.assert_called_once_with(180)
    mock_page2.rotate.assert_not_called()


@patch("os.path.exists", return_value=False)
def test_rotate_file_not_found(mock_exists):
    rotator = PdfRotator()
    with pytest.raises(FileNotFoundError):
        rotator.rotate("missing.pdf", 90)


@patch("os.path.exists", return_value=True)
def test_rotate_invalid_angle(mock_exists):
    rotator = PdfRotator()
    with pytest.raises(ValueError):
        rotator.rotate("dummy.pdf", 45)  # type: ignore
