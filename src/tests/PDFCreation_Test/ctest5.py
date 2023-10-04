import os
import pytest
from fitz import fitz
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


def test_footer(pdf_instance):
    # Act: Call the add_page method to create a page
    pdf_instance.add_page()

    # Call the footer method
    pdf_instance.footer()

    # Save the PDF to a temporary file
    pdf_filename = os.path.join(TEST_DIR, "test_footer.pdf")
    pdf_instance.output(pdf_filename)

    # Use PyMuPDF to extract text from the PDF
    pdf_document = fitz.open(pdf_filename)
    pdf_text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pdf_text += page.get_text()

    #  if the "Wasdi" link is added to the PDF footer
    expected_link = "Wasdi"
    assert expected_link in pdf_text


def test_chapter_title(pdf_instance):
    #  Call the add_page method to create a page
    pdf_instance.add_page()

    # Define test chapter number and title
    ch_num = 1
    ch_title = "Introduction"

    # Call the chapter_title method to add the chapter title to the page
    pdf_instance.chapter_title(ch_num, ch_title)

    # Save the PDF to a temporary file
    pdf_filename = os.path.join(TEST_DIR, "test_chapter_title.pdf")
    pdf_instance.output(pdf_filename)

    # Use PyMuPDF to extract text from the PDF
    pdf_document = fitz.open(pdf_filename)
    pdf_text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pdf_text += page.get_text()

    # Check if the expected chapter title text is present in the extracted text
    expected_text = f"Chapter {ch_num}: {ch_title}"
    assert expected_text in pdf_text


# Run the tests
if __name__ == "__main__":
    pytest.main([os.path.basename(__file__)])
