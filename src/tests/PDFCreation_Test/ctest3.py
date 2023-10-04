import pytest
from src.main.PDFReportCreation.CustomPDF import CustomPDF  # Import your CustomPDF class from your codebase


# Define a test function for the header method
def test_header_with_params():
    # Arrange
    params = {
        "cover_page": {
            "template_image_filename": "cover23.jpg",
            "alignment": "center",
        },
        "header": {
            "title": "WASDI FINAL REPORT",
            "logo": "wasdi_logo.jpg",
            "author_name": "Abdullah Al Foysal",
            "company_name": "UNIGE",
            "address": "16126, Genova, Italy",
            "website": "https://www.unige.it",
            "telephone": "+39 010 209XXXX",
            "company_address": "Company Address Here",
            "company_phone": "+1 123-456-7890",
        },
        "style": {
            "font_size": 13,
            "font_family": "Arial",
            "font_style": "I",
            "title_background": "#008000",
        },
    }
    pdf = CustomPDF(params)  # Create an instance of CustomPDF with the provided params

    # Act
    pdf.add_page()  # Add a page to the PDF
    pdf.header()  # Call the header method

    # Assert
    # You can add assertions here to check if the header content is as expected
    # For example, you can check if the title, author_name, company_name, etc., are present in the generated PDF


# Run the test using pytest
if __name__ == "__main__":
    pytest.main()
