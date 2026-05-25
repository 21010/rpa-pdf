import pytest
from rpa_pdf import Stamp, Pdf

@pytest.fixture
def stamp():
    return Stamp()

@pytest.fixture
def sample_pdf(tmp_path):
    file_path = tmp_path / "sample.pdf"
    pdf_instance = Pdf()
    pdf_instance.text_to_pdf("Test PDF", str(file_path))
    return str(file_path)

def test_generate_code39_stamp(stamp, tmp_path):
    out_file = tmp_path / "stamp.pdf"
    stamp.generate_code39_stamp('12345678', str(out_file), width=80, height=40)
    assert out_file.exists()

def test_add_code39_stamp(stamp, sample_pdf, tmp_path):
    out_file = tmp_path / "out.pdf"
    stamp.add_code39_stamp(sample_pdf, str(out_file), '10000000')
    assert out_file.exists()

def test_add_text_stamp(stamp, sample_pdf, tmp_path):
    out_file = tmp_path / "out2.pdf"
    stamp.add_text_stamp(sample_pdf, str(out_file), 'dupa')
    assert out_file.exists()