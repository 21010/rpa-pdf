import os
import pytest
from rpa_pdf import Converter

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "samples")


def get_sample_files():
    if not os.path.exists(DATA_DIR):
        return []
    files = []
    for filename in os.listdir(DATA_DIR):
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.isfile(filepath):
            files.append(filename)
    return files


@pytest.fixture
def converter():
    return Converter()


@pytest.mark.parametrize("filename", get_sample_files())
def test_convert_sample(converter, output_dir, filename):
    input_file = os.path.join(DATA_DIR, filename)

    # We append .pdf to the original filename to guarantee unique outputs
    # e.g., 'sample.jpg' -> 'test_sample.jpg.pdf'
    out_file = os.path.join(output_dir, f"test_{filename}.pdf")

    # The Converter class dynamically maps extensions to the correct engine
    result = converter.convert(input_file, out_file)

    # Verify that the converter handled the file and the PDF was generated
    assert result is True
    assert os.path.exists(out_file)
