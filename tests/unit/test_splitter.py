from unittest.mock import patch, MagicMock
import pytest
from rpa_pdf.pdf.splitter import PdfSplitter


@patch("os.path.exists", return_value=True)
@patch("builtins.open")
@patch("rpa_pdf.pdf.splitter.PdfReader")
@patch("rpa_pdf.pdf.splitter.PdfWriter")
def test_split_pdf(mock_writer, mock_reader, mock_open, mock_exists):
    mock_pdf = MagicMock()
    mock_page1 = MagicMock()
    mock_page2 = MagicMock()
    mock_pdf.pages = [mock_page1, mock_page2]
    mock_reader.return_value = mock_pdf

    mock_writer_instance = MagicMock()
    mock_writer.return_value = mock_writer_instance

    splitter = PdfSplitter()
    result = splitter.split("dummy.pdf", "output_dir")

    assert len(result) == 2
    assert mock_writer_instance.add_page.call_count == 2
    assert mock_writer_instance.write.call_count == 2


@patch("os.path.exists", return_value=False)
def test_split_file_not_found(mock_exists):
    splitter = PdfSplitter()
    with pytest.raises(FileNotFoundError):
        splitter.split("missing.pdf")
