import os
import pytest
from CustomPDF import CustomPDF


def test_footer():
    # Create an instance of CustomPDF with a sample footer configuration
    footer_params = {
        "company_link": "https://www.wasdi.cloud/",
        "footer_link_alignment": "left",
    }
    pdf = CustomPDF({"footer": footer_params})

    # Act
    pdf.add_page()  # Add a page to the PDF
    pdf.footer()  # Call the footer method

    # Assert
    # Check if the "Wasdi" link with the provided company link is added to the PDF footer
    expected_link = "Wasdi"
    assert pdf.links[0] == (
        10.0,
        pdf.h - 15.0,
        pdf.w - 20.0,
        10.0,
        "https://www.wasdi.cloud/",
        expected_link,
    )


# Run the test
if __name__ == "__main__":
    pytest.main([os.path.basename(__file__)])
