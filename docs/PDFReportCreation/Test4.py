from unittest.mock import patch, MagicMock
from myProcessor import CustomPDF, wasdi
import pytest


def create_pdf(filename, params):
    # Initialize the CustomPDF and wasdiLog objects
    custom_pdf = CustomPDF(
        params
    )  # Create an instance of CustomPDF with the provided params
    wasdi_log = wasdi.wasdiLog()  # Create an instance of wasdiLog

    # Call the add_cover_page method
    custom_pdf.add_cover_page()

    # Call the add_index method
    custom_pdf.add_index()

    # Call the oversized_images method (assuming it exists in the CustomPDF class)
    custom_pdf.oversized_images()

    # Save the PDF to the specified filename
    custom_pdf.save(filename)


# Your test class
class TestCreatePdf:
    @patch("myProcessor.CustomPDF")
    @patch("myProcessor.wasdi.wasdiLog")
    def test_create_pdf(self, wasdiLogMock, CustomPDFMock):
        # Mock CustomPDF and wasdiLog
        custom_pdf_instance = CustomPDFMock.return_value
        oversized_images_mock = MagicMock()  # Create a mock for oversized_images method
        custom_pdf_instance.oversized_images = (
            oversized_images_mock  # Assign the mock to oversized_images
        )

        # Define the provided parameters
        test_params = {
            "filename": "report",
            "cover_page": {
                "template_image_filename": "cover23.jpg",
                "alignment": "center",
            },
            "start_content_from_page": 2,
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
            "chapters": [
                {
                    "title": "Introduction",
                    "sections": [
                        {
                            "subtitle": "Section 1.1: Overview",
                            "content": "GeoServer has emerged as an instrumental tool in the geospatial domain, allowing professionals to share, process, and edit geospatial data. Its flexibility and interoperability have paved the way for a myriad of applications, one of the most pertinent being flood analysis. This report delves into the intricacies of how GeoServer, in conjunction with satellite data, is revolutionizing flood analysis.",
                            "image_path": "img.png",
                            "image_x": 80,
                            "image_y": 160,
                            "image_width": 100,
                            "image_height": 80,
                        }
                    ],
                    "tables": [
                        {
                            "data": [
                                ["Column 1", "Column 2", "Column 3"],
                                ["Data 1", "Data 2", "Data 3"],
                                ["Data A", "Data B", "Data C"],
                            ],
                            "col_widths": [40, 40, 40],
                            "table_x": 10,
                            "table_y": 10,
                            "table_width": 10,
                            "table_height": 10,
                        }
                    ],
                },
                {
                    "title": "Literature Review",
                    "sections": [
                        {
                            "subtitle": "Section 2.1: Previous Studies",
                            "content": "Historically, flood prediction relied heavily on ground data and early-warning systems. However, the advent of satellite technology has reshaped the dynamics of flood detection and prediction. Numerous studies have shed light on the efficacy of using satellites for this purpose, emphasizing faster response times and broader coverage. This section reviews existing literature, highlighting the advancements in satellite technology for flood detection, and how platforms like GeoServer are optimizing the use of this data.",
                            "image_path": "istockphoto-820339338-612x612.jpg",
                            "image_x": 80,
                            "image_y": 100,
                            "image_width": 60,
                            "image_height": 80,
                        }
                    ],
                    "tables": [
                        {
                            "data": [
                                ["Column A", "Column B"],
                                ["Value 1", "Value 2"],
                                ["Value X", "Value Y"],
                            ],
                            "col_widths": [60, 60],
                            "table_x": 10,
                            "table_y": 10,
                            "table_width": 10,
                            "table_height": 10,
                        }
                    ],
                },
                {
                    "title": "Methodology",
                    "sections": [
                        {
                            "subtitle": "Section 3.1: Research Design",
                            "content": "A multi-pronged research approach was adopted, entailing the analysis of satellite images, real-time flood data integration in GeoServer, and ground-truth verification. Our methodology also involved studying the spectral signatures of water bodies during flood events, enabling the differentiation between regular water bodies and flooded areas.",
                            "image_path": "",
                            "image_x": 30,
                            "image_y": 70,
                            "image_width": 100,
                            "image_height": 80,
                        },
                        {
                            "subtitle": "Section 3.2: Data Collection",
                            "content": "Satellite data was procured from various sources, primarily focusing on high-resolution imagery capable of detecting minute changes in water levels. Synthetic Aperture Radar (SAR) imagery, known for its cloud-penetrating capabilities, was especially valuable. Once collated, the data was integrated into GeoServer for detailed analysis and visualization.",
                            "image_path": "geo.jpg",
                            "image_x": 60,
                            "image_y": 90,
                            "image_width": 110,
                            "image_height": 70,
                        },
                    ],
                    "tables": [
                        {
                            "data": [
                                ["Header 1", "Header 2"],
                                ["Info A", "Info B"],
                                ["Info X", "Info Y"],
                            ],
                            "col_widths": [50, 50],
                            "table_x": 10,
                            "table_y": 10,
                            "table_width": 10,
                            "table_height": 10,
                        }
                    ],
                },
                {
                    "title": "Results",
                    "sections": [
                        {
                            "subtitle": "Section 4.1: Data Analysis",
                            "content": "Our analysis revealed that satellite imagery, when integrated into platforms like GeoServer, can significantly enhance flood prediction and monitoring. The high-resolution imagery allowed for precise demarcation of flooded areas, while GeoServer's rendering capabilities provided clear, actionable visuals. We also noted a marked reduction in response time, enabling quicker disaster management actions.",
                            "image_path": "rainfall in each month.png",
                            "image_x": 50,
                            "image_y": 60,
                            "image_width": 130,
                            "image_height": 110,
                        }
                    ],
                    "tables": [
                        {
                            "data": [
                                ["Value X", "Value Y"],
                                ["Value A", "Value B"],
                                ["Number 1", "Number 2"],
                            ],
                            "col_widths": [50, 50],
                            "table_x": 10,
                            "table_y": 10,
                            "table_width": 10,
                            "table_height": 10,
                        }
                    ],
                },
                {
                    "title": "Discussion",
                    "sections": [
                        {
                            "subtitle": "Section 5.1: Findings",
                            "content": "The confluence of satellite data and GeoServer has undeniably bolstered flood analysis capabilities. The granularity of satellite data ensures meticulous analysis, while GeoServer's robust platform allows for comprehensive data visualization. However, challenges like satellite revisit times and data latency remain. Addressing these can further optimize flood response mechanisms.",
                            "image_path": "img.png",
                            "image_x": 40,
                            "image_y": 70,
                            "image_width": 100,
                            "image_height": 90,
                        }
                    ],
                    "tables": [
                        {
                            "data": [
                                ["Category 1", "Category 2", "Category 3"],
                                ["Result A", "Result B", "Result C"],
                                ["Conclusion X", "Conclusion Y", "Conclusion Z"],
                            ],
                            "col_widths": [40, 40, 40],
                            "table_x": 10,
                            "table_y": 10,
                            "table_width": 10,
                            "table_height": 10,
                        }
                    ],
                },
                {
                    "title": "Conclusion",
                    "sections": [
                        {
                            "subtitle": "Section 6.1: Summary",
                            "content": "GeoServer, when augmented with satellite data, presents a formidable solution to the challenges of flood detection and monitoring. The synergy of these technologies holds promise for future advancements in disaster management. While there's potential for improvement, the current trajectory is undeniably progressive.",
                            "image_path": "GeoServer-service-and-geospatial-datasets-Satellite-dections-smoke-areas-and-red-flag.png",
                            "image_x": 30,
                            "image_y": 50,
                            "image_width": 160,
                            "image_height": 120,
                        }
                    ],
                    "tables": [
                        {
                            "data": [
                                ["Conclusion 1", "Conclusion 2"],
                                ["Summary X", "Summary Y"],
                                ["Final Thoughts", "Remarks"],
                            ],
                            "col_widths": [60, 60],
                            "table_x": 10,
                            "table_y": 10,
                            "table_width": 10,
                            "table_height": 10,
                        }
                    ],
                },
                {
                    "title": "Future Work",
                    "sections": [
                        {
                            "subtitle": "Section 7.1: Recommendations",
                            "content": "Future research can delve deeper into optimizing the integration of real-time satellite data with GeoServer. Exploring partnerships with satellite providers for quicker data feeds, enhancing GeoServer's processing capabilities for vast datasets, and expanding the application to other natural disasters are potential avenues for exploration.",
                            "image_path": "iQe86.png",
                            "image_x": 20,
                            "image_y": 40,
                            "image_width": 170,
                            "image_height": 130,
                        }
                    ],
                    "tables": [
                        {
                            "data": [
                                [
                                    "Recommendation 1",
                                    "Recommendation 2",
                                    "Recommendation 3",
                                ],
                                ["Suggestion A", "Suggestion B", "Suggestion C"],
                                ["Next Steps", "Exploration", "Prospects"],
                            ],
                            "col_widths": [40, 40, 40],
                            "table_x": 10,
                            "table_y": 10,
                            "table_width": 10,
                            "table_height": 10,
                        }
                    ],
                },
            ],
            "footer": {
                "company_link": "https://www.wasdi.cloud/",
                "footer_link_alignment": "left",
                "footer_page_number_alignment": "center",
            },
            "style": {
                "font_size": 13,
                "font_family": "Arial",
                "font_style": "I",
                "title_background": "#008000",
            },
        }

        # Call the create_pdf function
        create_pdf("test_output.pdf", test_params)

        # Assertions
        CustomPDFMock.assert_called_with(test_params)
        custom_pdf_instance.add_cover_page.assert_called_once()
        custom_pdf_instance.add_index.assert_called_once()
        oversized_images_mock.assert_called_once()  # Use oversized_images_mock for assertion


# Execute the tests
if __name__ == "__main__":
    pytest.main()
