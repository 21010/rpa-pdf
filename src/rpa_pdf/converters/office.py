import ctypes
import comtypes.client
from rpa_pdf.converters.base import BaseConverter


def _zero_com_pointer(obj):
    """Zeros out the raw COM pointer to prevent RPC crashes during __del__."""
    try:
        p = getattr(obj, "_comobj", obj)
        if p:
            ctypes.memset(ctypes.addressof(p), 0, ctypes.sizeof(p))
    except Exception:  # nosec B110
        pass


class ExcelConverter(BaseConverter):
    def convert(self, input_file_path: str, output_file_path: str | None = None) -> None:
        if not output_file_path:
            output_file_path = input_file_path + ".pdf"

        excel = comtypes.client.CreateObject("Excel.Application", dynamic=True)
        try:
            excel.Visible = False
            excel.DisplayAlerts = False

            workbooks = excel.Workbooks
            workbook = workbooks.Open(input_file_path)

            worksheets = workbook.Worksheets
            for sheet in worksheets:
                sheet.PageSetup.LeftMargin = excel.Application.InchesToPoints(0.25)
                sheet.PageSetup.RightMargin = excel.Application.InchesToPoints(0.25)
                sheet.PageSetup.TopMargin = excel.Application.InchesToPoints(0.75)
                sheet.PageSetup.BottomMargin = excel.Application.InchesToPoints(0.75)
                sheet.PageSetup.Orientation = 2
                sheet.PageSetup.Zoom = False
                sheet.PageSetup.FitToPagesWide = 1
                sheet.PageSetup.FitToPagesTall = 1

            workbook.ExportAsFixedFormat(0, output_file_path)

            try:
                workbook.Close(False)
            except Exception:  # nosec B110
                pass

            # Explicitly clear intermediate COM wrappers before quitting Excel
            _zero_com_pointer(sheet)
            _zero_com_pointer(worksheets)
            _zero_com_pointer(workbook)
            _zero_com_pointer(workbooks)
            del sheet
            del worksheets
            del workbook
            del workbooks
            import gc

            gc.collect()

        finally:
            if excel is not None:
                try:
                    excel.Quit()
                except Exception:  # nosec B110
                    pass
                _zero_com_pointer(excel)
                del excel
                import gc

                gc.collect()


class WordConverter(BaseConverter):
    def convert(self, input_file_path: str, output_file_path: str | None = None) -> None:
        if not output_file_path:
            output_file_path = input_file_path + ".pdf"

        word = comtypes.client.CreateObject("Word.Application", dynamic=True)
        try:
            word.Visible = False
            word.DisplayAlerts = 0  # wdAlertsNone

            documents = word.Documents
            doc = documents.Open(input_file_path, False, True, False)
            doc.ExportAsFixedFormat(output_file_path, 17)  # wdExportFormatPDF = 17

            try:
                doc.Close(False)
            except Exception:  # nosec B110
                pass

            # Explicitly clear intermediate COM wrappers before quitting Word
            _zero_com_pointer(doc)
            _zero_com_pointer(documents)
            del doc
            del documents
            import gc

            gc.collect()

        finally:
            if word is not None:
                try:
                    word.Quit()
                except Exception:  # nosec B110
                    pass
                _zero_com_pointer(word)
                del word
                import gc

                gc.collect()


class PowerPointConverter(BaseConverter):
    def convert(self, input_file_path: str, output_file_path: str | None = None) -> None:
        if not output_file_path:
            output_file_path = input_file_path + ".pdf"

        powerpoint = comtypes.client.CreateObject("PowerPoint.Application", dynamic=True)
        try:
            powerpoint.DisplayAlerts = 1  # ppAlertsNone = 1

            presentations = powerpoint.Presentations
            presentation = presentations.Open(input_file_path, False, False, False)
            presentation.SaveAs(output_file_path, 32)  # ppSaveAsPDF = 32

            try:
                presentation.Close()
            except Exception:  # nosec B110
                pass

            # Explicitly clear intermediate COM wrappers before quitting PowerPoint
            _zero_com_pointer(presentation)
            _zero_com_pointer(presentations)
            del presentation
            del presentations
            import gc

            gc.collect()

        finally:
            if powerpoint is not None:
                try:
                    powerpoint.Quit()
                except Exception:  # nosec B110
                    pass
                _zero_com_pointer(powerpoint)
                del powerpoint
                import gc

                gc.collect()
