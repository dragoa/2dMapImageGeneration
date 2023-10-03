import unittest
from CustomPDF import CustomPDF
import os


class TestCustomPDFAddCoverPage(unittest.TestCase):
    def test_add_cover_page_with_image(self):
        # Arrange
        params = {
            "cover_page": {
                "template_image_filename": "coverpage.jpg",
            },
            "header": {
                "title": "Test Title",  # Add a "title" key
            },
            "style": {},
            "footer": {},  # Add a dummy "footer" value
        }
        pdf = CustomPDF(params)

        # Act
        pdf.add_cover_page()

        # Assert
        self.assertTrue(pdf.cover_added)

    def test_add_cover_page_without_image(self):
        # Arrange
        params = {
            "cover_page": {},
            "header": {
                "title": "Test Title",  # Add a "title" key
            },
            "style": {},
            "footer": {},  # Add a dummy "footer" value
        }
        pdf = CustomPDF(params)

        # Act
        pdf.add_cover_page()

        # Assert
        self.assertTrue(pdf.cover_added)


if __name__ == "__main__":
    unittest.main()
