from unittest.mock import patch
from rpa_pdf.pdf.printer import PdfPrinter


@patch("os.path.exists", return_value=True)
@patch("subprocess.run")
def test_printer_pages_list(mock_run, mock_exists):
    printer = PdfPrinter()
    printer.print("dummy.pdf", pages=["1", "3"])
    args = mock_run.call_args[0][0]
    # args is a list of strings, e.g. ['sumatra.exe', '-print-to-default', '-print-settings', '1,3,portrait...']
    settings_arg = args[args.index("-print-settings") + 1]
    assert "1,3" in settings_arg


@patch("os.path.exists", return_value=True)
@patch("subprocess.run")
def test_printer_pages_first_last(mock_run, mock_exists):
    printer = PdfPrinter()
    printer.print("dummy.pdf", pages="first")
    args1 = mock_run.call_args[0][0]
    settings_arg1 = args1[args1.index("-print-settings") + 1]

    printer.print("dummy.pdf", pages="last")
    args2 = mock_run.call_args[0][0]
    settings_arg2 = args2[args2.index("-print-settings") + 1]

    assert "1" in settings_arg1.split(",")[0]
    assert "-1" in settings_arg2.split(",")[0]


@patch("os.path.exists", return_value=True)
@patch("subprocess.run")
def test_printer_odd_even(mock_run, mock_exists):
    printer = PdfPrinter()
    printer.print("dummy.pdf", odd_or_even="odd")
    printer.print("dummy.pdf", odd_or_even="even")
    assert mock_run.call_count == 2
