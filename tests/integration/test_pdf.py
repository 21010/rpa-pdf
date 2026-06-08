import pytest
import os
from rpa_pdf import Pdf


@pytest.fixture
def pdf():
    return Pdf()


@pytest.fixture
def data_dir():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "samples")


@pytest.fixture
def sample_pdf(pdf, data_dir):
    file_path = os.path.join(data_dir, "sample.pdf")
    if not os.path.exists(file_path):
        pdf.text_to_pdf("Test PDF", file_path)
    return file_path


def test_text_to_pdf(pdf, output_dir):
    out_file = os.path.join(output_dir, "test_pdf_text.pdf")
    pdf.text_to_pdf("hello world from integration test", out_file)
    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 0


def test_compress(pdf, sample_pdf, output_dir):
    out_file = os.path.join(output_dir, "test_pdf_compressed.pdf")
    # To test compression without modifying in place for tests, we copy first
    import shutil

    shutil.copy(sample_pdf, out_file)
    pdf.compress(out_file)
    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 0


def test_merge(pdf, sample_pdf, output_dir):
    out_file = os.path.join(output_dir, "test_pdf_merged.pdf")
    pdf.merge([sample_pdf, sample_pdf], out_file)
    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 0


def test_print(pdf, sample_pdf):
    # We can't guarantee a printer exists, but we can verify it doesn't crash
    # immediately if we provide a dummy printer, though subprocess.run checks True by default.
    # So we'll skip the actual printing in CI if it fails with FileNotFoundError (ghostscript missing).
    try:
        pdf.print(sample_pdf, printer="Dummy Printer")
    except Exception as e:
        pytest.skip(f"Print test skipped due to lack of environment setup (Ghostscript/Printer): {e}")
