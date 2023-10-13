import unittest
from unittest.mock import patch
import sys
import os

# Add the project root directory to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import the functions and classes you need to test
from src.main.PDFReportCreation.myProcessor import run, create_pdf

class TestRunFunction(unittest.TestCase):
    @patch("src.main.PDFReportCreation.myProcessor.create_pdf")
    @patch("src.main.PDFReportCreation.myProcessor.validate_parameters", return_value="output.pdf")
    def test_run(self, mock_validate_parameters, mock_create_pdf):
        # Mock the necessary functions and methods
        mock_create_pdf.return_value = None  # Mock the create_pdf function

        # Call the run() function
        run()

        # Assertions
        mock_validate_parameters.assert_called_once()
        mock_create_pdf.assert_called_with("output.pdf", {})

if __name__ == "__main__":
    unittest.main()
