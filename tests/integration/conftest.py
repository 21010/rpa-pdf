import pytest
import os


@pytest.fixture
def output_dir():
    """Provides a tests/output directory and creates it if it doesn't exist."""
    out_dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "results")
    os.makedirs(out_dir_path, exist_ok=True)
    return out_dir_path
