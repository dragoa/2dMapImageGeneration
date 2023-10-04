import uuid
import wasdi
from src.main.PDFReportCreation.CustomPDF import CustomPDF

# Define a function to create a PDF
def create_pdf(pdf_path, params):
    """
    Create a PDF document using the CustomPDF class.

    Parameters:
    pdf_path (str): The path to save the generated PDF.
    params (dict): A dictionary containing parameters for PDF generation.
    """
    pdf = CustomPDF(params)
    wasdi.wasdiLog("Creating PDF...")

    # Add the cover page before adding chapters
    pdf.add_cover_page()
    # Add the index before adding chapters
    pdf.add_index()

    for i, chapter in enumerate(params["chapters"], start=1):
        pdf.print_chapter(i, chapter["title"], chapter)

    pdf.oversized_images = "WARN"
    pdf.output(pdf_path)

    wasdi.wasdiLog("PDF created successfully")

# Define a function to create a blank PDF
def create_blank_pdf(pdf_path):
    """
    Create a blank PDF document with no content.

    Parameters:
    pdf_path (str): The path to save the generated blank PDF.
    """
    pdf = CustomPDF({})  # Create a CustomPDF object with empty parameters
    wasdi.wasdiLog("Creating blank PDF...")

    # Remove the header section
    pdf.asParametersDict["header"] = {}

    # Check if "footer" section exists in the parameters
    if "footer" not in pdf.asParametersDict:
        pdf.asParametersDict["footer"] = {}  # Add an empty "footer" section if not present

    pdf.add_page()
    pdf.output(pdf_path)
    wasdi.wasdiLog("Blank PDF created successfully")

# Define a function to sanitize parameters by removing leading/trailing whitespace
def sanitize_parameters(params):
    """
    Recursively remove leading/trailing whitespace from parameters.

    Parameters:
    params (str, list, dict): The input parameter(s) to sanitize.

    Returns:
    str, list, dict: The sanitized parameter(s).
    """
    if isinstance(params, str):
        return params.strip()
    elif isinstance(params, list):
        return [sanitize_parameters(item) for item in params]
    elif isinstance(params, dict):
        return {key: sanitize_parameters(value) for key, value in params.items()}
    else:
        return params

# Define a function to validate parameters
def validate_parameters(aoParams):
    """
    Validate parameters for PDF generation and set default values if needed.

    Parameters:
    aoParams (dict): A dictionary containing parameters for PDF generation.

    Returns:
    str: The validated or default filename for the PDF.
    """
    sFileName = aoParams.get("filename", "")
    if sFileName == "":
        sFileName = (str(uuid.uuid4()) + ".pdf")  # Generate a random UUID filename with ".pdf" extension
        wasdi.wasdiLog(
            f"FileName is not set or doesn't have the correct format! Generating a random UUID one... {sFileName}"
        )
    if not sFileName.endswith(".pdf"):
        sFileName = sFileName + ".pdf"
    aoParams["filename"] = sFileName

    # Validate cover_page
    cover_page = aoParams.get("cover_page", {})
    if not cover_page.get("template_image_filename"):
        wasdi.wasdiLog("Cover page template_image_filename is missing.")
        aoParams['cover_page'] = {}

    # Validate header
    header = aoParams.get("header", {})
    if not all(header.get(k) for k in ["title", "logo", "author_name", "company_name"]):
        wasdi.wasdiLog(
            "Header is missing one or more required fields (title, logo, author_name, company_name).")
        aoParams['header'] = {}

    # Validate chapters
    chapters = aoParams.get("chapters", [])
    if len(chapters) == 0:
        wasdi.wasdiLog("Chapters are empty")
        aoParams['chapters'] = []
    for chapter in chapters:
        if chapter.get("title") is None:
            chapter["title"] = "Default Title"

    # Validate footer
    footer = aoParams.get("footer", {})
    if not all(
            footer.get(k)
            for k in [
                "company_link",
                "footer_link_alignment",
                "footer_page_number_alignment",
            ]
    ):
        wasdi.wasdiLog("Footer is missing one or more required fields.")
        aoParams['footer'] = {}

    return sFileName

# Define the main function to run the PDF creation process
# Define the main function to run the PDF creation process
def run():
    """
    Main function to run the PDF generation process.
    """
    wasdi.wasdiLog("PDF tutorial v.1.4")
    aoParams = wasdi.getParametersDict()
    aoParams = sanitize_parameters(aoParams)
    sFileName = validate_parameters(aoParams)

    # Check if the parameters are empty, and if so, create a blank PDF
    if not aoParams or not aoParams["chapters"]:
        create_blank_pdf(sFileName)
    else:
        # Get the page number from the config.json file
        start_page = aoParams.get("start_content_from_page", 1)

        pdf = CustomPDF(aoParams)
        pdf.add_cover_page()
        pdf.add_index()

        # Add blank pages to reach the desired starting page
        for _ in range(start_page - 1):
            pdf.add_page()

        for i, chapter in enumerate(aoParams["chapters"], start=1):
            pdf.print_chapter(i, chapter["title"], chapter)

        pdf.oversized_images = "WARN"
        pdf.output(sFileName)

        wasdi.wasdiLog("PDF created successfully")


# Initialize WASDI
if __name__ == "__main__":
    wasdi.init("./config.json")
    run()
