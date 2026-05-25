import comtypes.client
from rpa_pdf.converters.base import BaseConverter

class ExcelConverter(BaseConverter):
    def convert(self, input_file_path: str, output_file_path: str | None = None) -> None:
        try:
            excel = comtypes.client.CreateObject('Excel.Application')
            excel.Visible = False
            excel.DisplayAlerts = False
            
            workbook = excel.Workbooks.Open(input_file_path)
            for sheet in workbook.Worksheets:
                sheet.PageSetup.LeftMargin = excel.Application.InchesToPoints(0.25)
                sheet.PageSetup.RightMargin = excel.Application.InchesToPoints(0.25)
                sheet.PageSetup.TopMargin = excel.Application.InchesToPoints(0.75)
                sheet.PageSetup.BottomMargin = excel.Application.InchesToPoints(0.75)
                sheet.PageSetup.Orientation = 2
                sheet.PageSetup.Zoom = False
                sheet.PageSetup.FitToPagesWide = 1
                sheet.PageSetup.FitToPagesTall = 1

            workbook.ExportAsFixedFormat(0, output_file_path)
        except Exception as ex:
            raise ex
        finally:
            try:
                workbook.Close(False)
                excel.Quit()
            except Exception:
                pass  # nosec B110

class WordConverter(BaseConverter):
    def convert(self, input_file_path: str, output_file_path: str | None = None) -> None:
        try:
            word = comtypes.client.CreateObject('Word.Application')
            word.Visible = False
            word.DisplayAlerts = False
            
            doc = word.Documents.Open(input_file_path)
            # wdFormatPDF = 17
            doc.SaveAs(output_file_path, FileFormat=17)
        except Exception as ex:
            raise ex
        finally:
            try:
                doc.Close(False)
                word.Quit()
            except Exception:
                pass  # nosec B110

class PowerPointConverter(BaseConverter):
    def convert(self, input_file_path: str, output_file_path: str | None = None) -> None:
        try:
            powerpoint = comtypes.client.CreateObject('PowerPoint.Application')
            powerpoint.DisplayAlerts = 1 # ppAlertsNone = 1
            # ppSaveAsPDF = 32
            presentation = powerpoint.Presentations.Open(input_file_path, WithWindow=False)
            presentation.SaveAs(output_file_path, 32)
        except Exception as ex:
            raise ex
        finally:
            try:
                presentation.Close()
                powerpoint.Quit()
            except Exception:
                pass  # nosec B110
