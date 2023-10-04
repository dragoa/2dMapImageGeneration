import unittest
import json
from io import StringIO
import sys

# Import the functions from your main script
from src.main.PDFReportCreation.myProcessor import sanitize_parameters, validate_parameters


class TestParameterValidation(unittest.TestCase):
    def setUp(self):
        # Redirect Wasdi log output to a StringIO buffer
        self.log_output = StringIO()
        sys.stdout = self.log_output

    def tearDown(self):
        # Restore the standard output
        sys.stdout = sys.__stdout__

    def test_valid_parameters(self):
        # Load parameters from a JSON file
        with open("params.json", "r") as file:
            params = json.load(file)

        # Call the validate_parameters function
        validated_filename = validate_parameters(params)

        # Assert that the filename is valid (matches the expected pattern)
        self.assertTrue(validated_filename.endswith(".pdf"))


if __name__ == "__main__":
    unittest.main()
