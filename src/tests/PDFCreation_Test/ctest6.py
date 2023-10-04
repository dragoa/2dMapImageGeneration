import os
import pytest
from fitz import fitz
from PIL import Image
from src.main.PDFReportCreation.CustomPDF import CustomPDF

# Define a test directory where temporary PDF files will be stored
TEST_DIR = "tests"

# Ensure the test directory exists
os.makedirs(TEST_DIR, exist_ok=True)


@pytest.fixture
def pdf_instance():
    # Create an instance of CustomPDF for testing with footer configuration
    footer_config = {
        "footer": {
            "company_link": "https://www.wasdi.cloud/",
            "footer_link_alignment": "left",
            "footer_page_number_alignment": "center",
        }
    }
    return CustomPDF(footer_config)


def test_fit_image(pdf_instance):
    # Act: Call the add_page method to create a page
    pdf_instance.add_page()

    # Define image path and coordinates
    img_path = "geo.jpg"
    x = 10
    y = 10
    w = 100
    h = 100

    # Call the fit_image method to fit the image within the bounding box
    pdf_instance.fit_image(img_path, x, y, w, h)

    # Save the PDF to a temporary file
    pdf_filename = os.path.join(TEST_DIR, "test_fit_image.pdf")
    pdf_instance.output(pdf_filename)

    # Assert: Check if the image is added to the PDF
    pdf_document = fitz.open(pdf_filename)
    assert pdf_document.page_count == 1  # Ensure there is one page in the PDF


def test_chapter_body(pdf_instance):
    # Act: Call the add_page method to create a page
    pdf_instance.add_page()

    # Define chapter data with sections
    chapter_data = {
        "sections": [
            {
                "subtitle": "Section 1",
                "content": "This is the content of section 1.",
                "image_path": "geo.jpg",
                "image_x": 10,
                "image_y": 10,
                "image_width": 100,
                "image_height": 100,
            },
            {
                "subtitle": "Section 2",
                "content": "This is the content of section 2.",
                "image_path": "geo.jpg",
                "image_x": 20,
                "image_y": 20,
                "image_width": 80,
                "image_height": 80,
            },
        ]
    }

    # Call the chapter_body method to add the chapter content to the page
    pdf_instance.chapter_body(chapter_data)

    # Save the PDF to a temporary file
    pdf_filename = os.path.join(TEST_DIR, "test_chapter_body.pdf")
    pdf_instance.output(pdf_filename)

    # Assert: Check if the generated PDF contains the specified sections and images
    pdf_document = fitz.open(pdf_filename)
    assert pdf_document.page_count == 1  # Ensure there is one page in the PDF


# Run the tests
if __name__ == "__main__":
    pytest.main([os.path.basename(__file__)])
