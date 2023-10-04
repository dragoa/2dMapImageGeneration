import unittest
import uuid
import json
import re
from src.main.PDFReportCreation.myProcessor import validate_parameters


def read_parameters_from_json(json_file):
    # Read parameters from the JSON file
    with open(json_file, "r") as file:
        params = json.load(file)
    return params


class TestValidateParameters(unittest.TestCase):

    def test_valid_parameters(self):
        # Read parameters from the JSON file
        params = read_parameters_from_json("config.json")

        # Call the validate_parameters function
        validated_filename = validate_parameters(params)

        # Assert that the filename is valid (matches the expected pattern)
        self.assertTrue(re.match(r"^[a-f0-9-]+report\.pdf$", validated_filename))

    def test_missing_filename(self):
        # Create a dictionary with missing filename
        missing_filename_params = {
            "cover_page": {
                "template_image_filename": "cover23.jpg",
                "alignment": "center",
            }
        }

        # Call the validate_parameters function
        validated_filename = validate_parameters(missing_filename_params)

        # Assert that the function generates a random filename with ".pdf" extension
        self.assertTrue(validated_filename.endswith(".pdf"))

    def test_missing_cover_page(self):
        # Create a dictionary with missing cover_page
        missing_cover_page_params = {
            "filename": "report",
            # ...
        }

        # Call the validate_parameters function
        validated_filename = validate_parameters(missing_cover_page_params)

        # Assert that the function generates a random filename with ".pdf" extension
        self.assertTrue(validated_filename.endswith(".pdf"))


if __name__ == "__main__":
    unittest.main()
