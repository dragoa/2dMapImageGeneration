import unittest
from src.main.PDFReportCreation.CustomPDF import CustomPDF  # Import the CustomPDF class from your module


class TestCustomPDF(unittest.TestCase):
    def test_add_table_and_print_chapter(self):
        # Create a valid configuration with a 'footer' key
        config = {
            "footer": {
                # Define any required footer parameters here
                "footer_page_number_alignment": "C"
            }
        }

        # Create an instance of CustomPDF with the valid configuration
        pdf = CustomPDF(config)

        # Define test chapter number and title
        ch_num = 1
        ch_title = "Test Chapter"

        # Define test_chapter_data with appropriate content
        test_chapter_data = {
            "sections": [
                {
                    "subtitle": "Subsection 1",
                    "content": "This is the content of subsection 1",
                    # Add other subsection data as needed
                },
                # Add more sections as needed
            ],
            "tables": [
                {
                    "data": [
                        # Define table data as a list of lists
                        ["Header 1", "Header 2", "Header 3"],
                        ["Data 1", "Data 2", "Data 3"],
                        # Add more rows as needed
                    ],
                    "col_widths": [40, 40, 40],  # Define column widths
                    # Add other table parameters as needed
                },
                # Add more tables as needed
            ],
        }

        # Act: Call the print_chapter method with the test chapter data
        pdf.print_chapter(ch_num, ch_title, test_chapter_data)

        # Assert: Check if the chapter title and table are added to the PDF
        pdf_filename = "test_table.pdf"
        pdf.output(pdf_filename)
        # You can add further assertions to check the content of the generated PDF if needed


if __name__ == "__main__":
    unittest.main()
