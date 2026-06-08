# PDF documents operations library

![RPA Automation](https://img.shields.io/badge/RPA-Automation-0052cc?style=for-the-badge)
![Robocorp Compatible](https://img.shields.io/badge/Robocorp-Compatible-success?style=for-the-badge)
![uv](https://img.shields.io/badge/uv-Package_Manager-purple?style=for-the-badge)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?style=for-the-badge)
![Coverage 85%](https://img.shields.io/badge/coverage-85%25-brightgreen?style=for-the-badge)
![Security: Bandit](https://img.shields.io/badge/security-bandit-yellow.svg?style=for-the-badge)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge)
![CI Testing](https://img.shields.io/github/actions/workflow/status/21010/rpa-pdf/ci.yml?branch=master&label=CI&style=for-the-badge)

Python module that delivers a comprehensive set of actions to manipulate and convert files to PDF. It is specifically designed to be easily integrated into Robotic Process Automation (RPA) workflows.

The module is natively compatible with **Robocorp** and provides streamlined abstractions over complex PDF tasks.

## Business Capabilities

`rpa-pdf` accelerates your automation projects by providing out-of-the-box features for:
* **Universal Document Conversion**: Convert Office documents (Word, Excel, PowerPoint), HTML, Text, Emails (`.msg`, `.eml`), and Images into standard PDF formats without manual intervention.
* **Document Manipulation**: Merge, compress, split, and rotate PDF files.
* **Content Extraction**: Rip raw text or embedded images directly out of PDF pages.
* **Compliance & Stamping**: Automatically stamp PDFs with text (watermarks) or Code39 barcodes (useful for invoice tracking, archiving, and indexing).
* **Automated Printing**: Send PDFs directly to physical or virtual printers without UI prompts.

## Architecture & Structure

The package is built with a modular architecture leveraging robust Python libraries (`pypdf`, `fpdf2`, `Pillow`, `comtypes`, `xhtml2pdf`, `extract-msg`) abstracted behind a simple, RPA-friendly API.

* **`rpa_pdf.Pdf`**: The core facade exposing primary manipulation methods (`merge`, `compress`, `print`) and text-to-PDF capabilities.
* **`rpa_pdf.Stamp`**: Utilities focused entirely on adding text and barcode overlays onto existing documents.
* **`rpa_pdf.Converter`**: A universal registry-based format converter that dynamically proxies out to appropriate engines based on file extensions.
* **`rpa_pdf.TextExtractor` & `rpa_pdf.ImageExtractor`**: Extract embedded content from PDFs.
* **`rpa_pdf.PdfSplitter` & `rpa_pdf.PdfRotator`**: Handle page-level PDF mutations.
* **Bundled Executables**: Bundles necessary fonts and lightweight viewers (like `SumatraPDF`) to guarantee predictable cross-environment execution, especially for silent printing operations.

## Installation

We recommend using a modern package manager like `uv` or standard `pip`.

```bash
# Using pip
pip install rpa-pdf

# Using uv
uv pip install rpa-pdf
```

## Examples

### 1. Universal File Conversions (Word/Excel/PowerPoint/HTML/Email/Images)
The simplest way to convert any supported format into a PDF is using the universal `Converter` class. 
*(Note: Office conversion requires Microsoft Office to be installed on the machine)*
```python
from rpa_pdf import Converter

converter = Converter()

# Converts Word documents
converter.convert('c:/temp/document.docx', 'c:/temp/document.pdf')

# Converts Excel spreadsheets
converter.convert('c:/temp/data.xlsx') # Defaults to c:/temp/data.xlsx.pdf

# Converts Emails (.eml, .msg)
converter.convert('c:/temp/email.msg', 'c:/temp/email.pdf')

# Converts HTML & Images
converter.convert('c:/temp/index.html', 'c:/temp/website.pdf')
converter.convert('c:/temp/scan.png', 'c:/temp/scan.pdf')
```

### 2. Merging PDF Files
Combine multiple invoice documents into one package.
```python
from rpa_pdf import Pdf

pdf = Pdf()
pdf.merge(['c:/temp/invoice_1.pdf', 'c:/temp/invoice_2.pdf'], 'c:/temp/merged_invoices.pdf')
```

### 3. Adding Text and Barcode Stamps
Great for adding tracking codes or "CONFIDENTIAL" watermarks to documents before they are printed or archived.
```python
from rpa_pdf import Stamp

stamp = Stamp()

# Add a text watermark to the center of the first page
stamp.add_text_stamp(
    input_pdf_file_path='c:/temp/input.pdf',
    output_pdf_file_path='c:/temp/watermarked.pdf',
    text='CONFIDENTIAL',
    font_size=40,
    text_horizontal_position='center',
    text_vertical_position='center'
)

# Add a Code39 tracking barcode
stamp.add_code39_stamp(
    input_pdf_file_path='c:/temp/input.pdf', 
    output_pdf_file_path='c:/temp/barcoded.pdf', 
    code='12345678',
    vertical_position='top',
    horizontal_position='right'
)
```

### 4. Splitting & Rotating PDFs
Extract individual pages from a large batch document or fix scanned orientations.
```python
from rpa_pdf import PdfSplitter, PdfRotator

# Split all pages into individual files
splitter = PdfSplitter()
splitter.split('c:/temp/batch_invoices.pdf', 'c:/temp/output_folder')

# Rotate the first page 90 degrees
rotator = PdfRotator()
rotator.rotate('c:/temp/scanned_doc.pdf', angle=90, pages='first')
```

### 5. Content Extraction
Pull text and embedded images out of a PDF.
```python
from rpa_pdf import TextExtractor, ImageExtractor

text_extractor = TextExtractor()
text = text_extractor.extract_text('c:/temp/document.pdf', pages=[0, 1])

img_extractor = ImageExtractor()
img_extractor.extract_images('c:/temp/document.pdf', 'c:/temp/images')
```

### 6. Generate PDF from Raw Text
Directly write string contents to a brand new PDF document.
```python
from rpa_pdf import Pdf

pdf = Pdf()
pdf.text_to_pdf(text="Automated report execution successful.", output_file_path="c:/temp/report.pdf")
```

### 7. Compressing a PDF File
Reduce the file size of a PDF before sending it via email.
```python
from rpa_pdf import Pdf

pdf = Pdf()
pdf.compress('c:/temp/large_file.pdf')
```

### 8. Print a PDF Silently
Print directly to a named printer using the bundled SumatraPDF engine.
```python
from rpa_pdf import Pdf

pdf = Pdf()
pdf.print('c:/temp/document.pdf', 'printer_name')
```

## Development & Testing

This project uses `uv` for dependency management and `ruff` for linting. Tests are run via `pytest`.

```bash
# Install dependencies including development extras
uv sync --all-extras

# Run tests
pytest
```
