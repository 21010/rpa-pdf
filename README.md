# PDF documents operations library

![RPA Automation](https://img.shields.io/badge/RPA-Automation-0052cc?style=for-the-badge)
![Robocorp Compatible](https://img.shields.io/badge/Robocorp-Compatible-success?style=for-the-badge)
![uv](https://img.shields.io/badge/uv-Package_Manager-purple?style=for-the-badge)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge)
![CI Testing](https://img.shields.io/github/actions/workflow/status/21010/rpa-pdf/ci.yml?branch=master&label=CI&style=for-the-badge)

Python module that delivers a comprehensive set of actions to manipulate and convert files to PDF. It is specifically designed to be easily integrated into Robotic Process Automation (RPA) workflows.

The module is natively compatible with **Robocorp** and provides streamlined abstractions over complex PDF tasks.

## Business Capabilities

`rpa-pdf` accelerates your automation projects by providing out-of-the-box features for:
* **Document Conversion**: Convert Office documents (Word, Excel, PowerPoint), HTML, Text, Emails, and Images into standard PDF formats without manual intervention.
* **Document Manipulation**: Merge multiple PDF files into a single document or compress heavy PDFs for storage and email transmission.
* **Compliance & Stamping**: Automatically stamp PDFs with text or Code39 barcodes (useful for invoice tracking, archiving, and indexing).
* **Automated Printing**: Send PDFs directly to physical or virtual printers without UI prompts.

## Architecture & Structure

The package is built with a modular architecture leveraging robust Python libraries (`pypdf`, `fpdf2`, `Pillow`, `comtypes`, `xhtml2pdf`, `extract-msg`) abstracted behind a simple, RPA-friendly API.

* **`rpa_pdf.Pdf`**: The core facade exposing primary manipulation methods (`merge`, `compress`, `print`) and text-to-PDF capabilities.
* **`rpa_pdf.Stamp`**: Utilities focused entirely on adding text and barcode overlays onto existing documents.
* **`rpa_pdf.converters.*`**: Specialized modules to handle complex format translations (e.g., interacting with COM objects for Office conversion or rendering HTML).
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

### 1. Merging PDF Files
Combine multiple invoice documents into one package.
```python
from rpa_pdf import Pdf

pdf = Pdf()
pdf.merge(['c:/temp/invoice_1.pdf', 'c:/temp/invoice_2.pdf'], 'c:/temp/merged_invoices.pdf')
```

### 2. File Conversions (Word/Excel/HTML/Images)
You can easily convert various documents to PDF.
*(Note: Office conversion requires Microsoft Office to be installed on the machine)*
```python
from rpa_pdf.converters import office, html, image

# Convert Word document to PDF
office.word_to_pdf('c:/temp/document.docx', 'c:/temp/document.pdf')

# Convert HTML to PDF
html.html_to_pdf('<h1>Hello World</h1>', 'c:/temp/output.pdf')

# Convert Image to PDF
image.image_to_pdf('c:/temp/scan.png', 'c:/temp/scan.pdf')
```

### 3. Adding a Code39 Barcode Stamp
Great for adding tracking codes to documents before they are printed or archived.
```python
from rpa_pdf import Pdf

pdf = Pdf()
pdf.add_code39_stamp(
    input_pdf='c:/temp/input_file.pdf', 
    output_pdf='c:/temp/stamped_file.pdf', 
    barcode_value='12345678'
)
```

### 4. Compressing a PDF File
Reduce the file size of a PDF before sending it via email.
```python
from rpa_pdf import Pdf

pdf = Pdf()
pdf.compress('c:/temp/large_file.pdf')
```

### 5. Print a PDF Silently
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
