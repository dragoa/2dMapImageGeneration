import unittest
from unittest.mock import patch, MagicMock
import json

# Import CustomPDF and wasdi from the correct module
from src.main.PDFReportCreation.CustomPDF import CustomPDF
import wasdi

def create_pdf(pdf_path, params):
    pdf = CustomPDF(params)
    wasdi.wasdiLog("Creating PDF...")

    # Add the cover page before adding chapters
    pdf.add_cover_page()
    # Add the index before adding chapters
    pdf.add_index()

    for i, chapter in enumerate(params["chapters"], start=1):
        pdf.print_chapter(i, chapter["title"], chapter)

    pdf.output(pdf_path)

    wasdi.wasdiLog("PDF created successfully")

class TestCreatePdf(unittest.TestCase):
    @patch("src.main.PDFReportCreation.CustomPDF.CustomPDF")
    @patch("wasdi.wasdiLog")
    def test_create_pdf(self, wasdiLogMock, CustomPDFMock):
        # Mock CustomPDF and wasdiLog
        custom_pdf_instance = CustomPDFMock.return_value

        # Load test parameters from JSON file
        with open('params.json', 'r') as params_file:
            test_params = json.load(params_file)

        # Call the create_pdf function
        create_pdf("test_output.pdf", test_params)

if __name__ == "__main__":
    unittest.main()
