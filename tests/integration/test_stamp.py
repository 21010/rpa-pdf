import pytest
import os
from rpa_pdf import Stamp, Pdf


@pytest.fixture
def stamp():
    return Stamp()


@pytest.fixture
def data_dir():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "samples")


@pytest.fixture
def sample_pdf(data_dir):
    file_path = os.path.join(data_dir, "sample_stamp.pdf")
    if not os.path.exists(file_path):
        pdf = Pdf()
        pdf.text_to_pdf("Test PDF for Stamping", file_path)
    return file_path


def test_generate_code39_stamp(stamp, output_dir):
    out_file = os.path.join(output_dir, "test_stamp_generated.pdf")
    stamp.generate_code39_stamp("12345678", out_file, width=80, height=40)
    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 0


def test_add_code39_stamp(stamp, sample_pdf, output_dir):
    out_file = os.path.join(output_dir, "test_stamp_added_code39.pdf")
    stamp.add_code39_stamp(sample_pdf, out_file, "10000000")
    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 0


def test_add_text_stamp(stamp, sample_pdf, output_dir):
    out_file = os.path.join(output_dir, "test_stamp_added_text.pdf")
    stamp.add_text_stamp(sample_pdf, out_file, "CONFIDENTIAL")
    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 0
