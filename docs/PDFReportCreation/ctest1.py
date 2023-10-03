import unittest
from CustomPDF import CustomPDF  # Replace with your actual module import


class TestCustomPDFInit(unittest.TestCase):
    def test_init_with_valid_params(self):
        # Arrange
        params = {
            "cover_page": {},
            "header": {},
            "style": {"font_size": 12},
        }

        # Act
        pdf = CustomPDF(params)

        # Assert
        self.assertEqual(pdf.asParametersDict, params)
        self.assertEqual(pdf.oCoverPage, params["cover_page"])
        self.assertEqual(pdf.oHeader, params["header"])
        self.assertEqual(pdf.oStyle, params["style"])
        self.assertFalse(pdf.index_added)
        self.assertFalse(pdf.cover_added)

    def test_init_with_missing_params(self):
        # Arrange
        params = {}

        # Act
        pdf = CustomPDF(params)

        # Assert
        self.assertEqual(pdf.asParametersDict, params)
        self.assertIsNone(pdf.oCoverPage)
        self.assertIsNone(pdf.oHeader)
        self.assertEqual(pdf.oStyle, {})  # Empty dict should be assigned
        self.assertFalse(pdf.index_added)
        self.assertFalse(pdf.cover_added)


if __name__ == "__main__":
    unittest.main()
