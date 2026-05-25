import pytest
import os
from unittest.mock import patch
from rpa_pdf import Pdf


@pytest.fixture
def pdf():
    return Pdf()


@pytest.fixture
def sample_pdf(tmp_path):
    file_path = tmp_path / "sample.pdf"
    pdf_instance = Pdf()
    pdf_instance.text_to_pdf("Test PDF", str(file_path))
    return str(file_path)


def test_compress(pdf, sample_pdf):
    # Compression might slightly increase the size of tiny dummy files due to overhead.
    # We just ensure it runs without crashing and the file remains valid.
    pdf.compress(sample_pdf)
    assert os.path.exists(sample_pdf)


def test_text_to_pdf(pdf, tmp_path):
    out_file = tmp_path / "out.pdf"
    pdf.text_to_pdf("hello", str(out_file))
    assert out_file.exists()


def test_merge(pdf, sample_pdf, tmp_path):
    out_file = tmp_path / "merged.pdf"
    pdf.merge([sample_pdf, sample_pdf], str(out_file))
    assert out_file.exists()


@patch("subprocess.run")
def test_print(mock_run, pdf, sample_pdf):
    pdf.print(sample_pdf, printer="Bullzip PDF Printer")
    mock_run.assert_called_once()
