import json
import pytest
from src.main.PDFReportCreation.CustomPDF import CustomPDF  # Import your CustomPDF class from your codebase

# Read the JSON data from the file
with open("params.json", "r") as json_file:
    params = json.load(json_file)


# Define a test function for the add_index and generate_index methods
def test_add_index_and_generate_index():
    # Create an instance of CustomPDF with the provided params
    pdf = CustomPDF(params)

    # Act
    pdf.add_page()  # Add a page to the PDF
    pdf.add_index()  # Call the add_index method to add an index
    generated_index = (
        pdf.generate_index()
    )  # Call the generate_index method to get the generated index

    # Assert
    # Check if the generated index contains the chapter titles
    for i, chapter in enumerate(params["chapters"], start=1):
        expected_entry = f'Chapter {i}: {chapter["title"]}\n'
        assert expected_entry in generated_index


# Run the test using pytest
if __name__ == "__main__":
    pytest.main()
