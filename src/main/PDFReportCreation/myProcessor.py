import wasdi
import os
from fpdf import FPDF
from PIL import Image


class CustomPDF(FPDF):
    # Template for creating the pdf report
    def __init__(self, params):
        super().__init__()
        self.asParametersDict = params

    def header(self):
        # Getting the parameters for the header
        osHeaderParams = self.asParametersDict['HEADER']
        sTitle = osHeaderParams['TITLE']
        sLogo = osHeaderParams['LOGO']
        sName = osHeaderParams['NAME']
        sCompanyName = osHeaderParams['COMPANY_NAME']
        sAddress = osHeaderParams['ADDRESS']

        # Set logo
        self.image(sLogo, x=10, y=10, w=30)

        # Set header title
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, sTitle, border=0, ln=1, align='C')

        # Set name and company
        self.set_font('Helvetica', '', 12)
        self.cell(0, 5, '', ln=1, align='R')  # Empty cell for alignment
        self.cell(0, 5, f'Author: {sName}', ln=1, align='R')
        self.cell(0, 5, f'Company: {sCompanyName}', ln=1, align='R')
        self.cell(0, 5, f'Address: {sAddress}', ln=1, align='R')
        self.ln(10)

    def footer(self):
        self.set_y(-10)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def chapterTitle(self, ch_num, ch_title):
        self.set_fill_color(34, 139, 34)  # Set fill color to green
        self.set_text_color(255)  # Set text color to white
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, f'Chapter {ch_num}: {ch_title}', ln=1, fill=True)
        self.ln()

    def chapterBody(self, oChapterData):
        self.set_fill_color(255)  # Set fill color back to white
        self.set_text_color(0)  # Set text color back to black
        self.set_font('Times', '', 12)

        aoChapterSections = oChapterData.get('SECTIONS', [])
        for section in aoChapterSections:
            sSubtitle = section.get('SUBTITLE')
            sContent = section.get('CONTENT')
            sImageFile = section.get('IMAGE_PATH')

            # Print subtitle
            self.set_font('Helvetica', 'B', 12)
            self.cell(0, 5, sSubtitle, ln=1, fill=True)
            self.ln()

            # Print content
            self.set_font('Times', '', 12)
            self.multi_cell(0, 10, sContent)
            self.ln(10)

            # Add image if specified
            if sImageFile:
                if os.path.exists(sImageFile):
                    # Calculate the available width for the image
                    available_width = self.w - self.l_margin - self.r_margin

                    # Load the image using PIL to get its dimensions
                    image = Image.open(sImageFile)
                    image_width, image_height = image.size

                    # Calculate the scale factor for resizing the image
                    scale_factor = available_width / image_width

                    # Calculate the scaled dimensions for the image
                    scaled_width = image_width * scale_factor
                    scaled_height = image_height * scale_factor

                    # Calculate the position to center the image vertically
                    image_y = self.get_y()

                    # Set the position for the image and print it
                    self.image(sImageFile, x=self.l_margin, y=image_y, w=scaled_width, h=scaled_height)
                else:
                    wasdi.wasdiLog(f"[WARNING] Image file not found: {sImageFile}")

    def print_chapter(self, ch_num, ch_title, chapter_data):
        self.add_page()
        self.chapterTitle(ch_num, ch_title)
        self.chapterBody(chapter_data)


def createPdf(pdf_path, params):
    pdf = CustomPDF(params)

    for key, value in params.items():
        wasdi.wasdiLog(f"{key}: {pdf.asParametersDict[key]}")

    # pdf.set_author('Abdullah Al Foysal')

    pdf.add_page()

    for i, chapter in enumerate(params['CHAPTERS'], start=1):
        pdf.print_chapter(i, chapter['TITLE'], chapter)

    pdf.output(pdf_path)


def validateParameters(params):
    # Check of the parameters
    if 'PDF_PATH' not in params:
        wasdi.wasdiLog("[WARNING] The PDF path is missing.")
        params['PDF_PATH'] = 'wasdi_final_report.pdf'  # Assign a default value
    else:
        if not params['PDF_PATH'].endswith('.pdf'):
            wasdi.wasdiLog("[WARNING] 'pdf_path' should have a '.pdf' extension.")
            # params['PDF_PATH'] += '.pdf'

    if 'HEADER' not in params:
        wasdi.wasdiLog("[WARNING] The header is missing.")
        params['HEADER'] = {}  # Assign an empty dictionary

    header = params['HEADER']
    if 'TITLE' not in header:
        wasdi.wasdiLog("[WARNING] The title of the header is missing.")
        header['TITLE'] = 'WASDI FINAL REPORT'  # Assign a default value

    if 'LOGO' not in header:
        wasdi.wasdiLog("[WARNING] The logo is missing in the header.")
        header['LOGO'] = 'wasdi_logo.jpg'  # Assign a default value

    if 'NAME' not in header:
        wasdi.wasdiLog("[WARNING] 'name' is missing in the header.")
        header['NAME'] = ''  # Assign an empty string

    if 'COMPANY_NAME' not in header:
        wasdi.wasdiLog("[WARNING] 'company_name' is missing in the header.")
        header['COMPANY_NAME'] = ''  # Assign an empty string

    if 'ADDRESS' not in header:
        wasdi.wasdiLog("[WARNING] 'address' is missing in the header.")
        header['ADDRESS'] = ''  # Assign an empty string

    if 'CHAPTERS' not in params:
        wasdi.wasdiLog("[WARNING] 'chapters' is missing in the parameters.")
        params['CHAPTERS'] = []  # Assign an empty list

    for chapter in params['CHAPTERS']:
        if 'TITLE' not in chapter:
            wasdi.wasdiLog("[WARNING] 'title' is missing in a chapter.")
            chapter['TITLE'] = ''  # Assign an empty string

        if 'SECTIONS' not in chapter:
            wasdi.wasdiLog("[WARNING] 'sections' is missing in a chapter.")
            chapter['SECTIONS'] = []  # Assign an empty list

        for section in chapter['SECTIONS']:
            if 'SUBTITLE' not in section:
                wasdi.wasdiLog("[WARNING] 'subtitle' is missing in a section.")
                section['SUBTITLE'] = ''  # Assign an empty string

            if 'CONTENT' not in section:
                wasdi.wasdiLog("[WARNING] 'content' is missing in a section.")
                section['CONTENT'] = ''  # Assign an empty string

            if 'IMAGE_PATH' not in section:
                wasdi.wasdiLog("[WARNING] 'image_path' is missing in a section.")
                section['IMAGE_PATH'] = ''  # Assign an empty string

    return params


def sanitizeParameters(params):
    params['PDF_PATH'] = params['PDF_PATH'].strip()  # Remove leading/trailing whitespace

    header = params['HEADER']
    header['TITLE'] = header['TITLE'].strip()
    header['LOGO'] = header['LOGO'].strip()
    header['NAME'] = header['NAME'].strip()
    header['COMPANY_NAME'] = header['COMPANY_NAME'].strip()
    header['ADDRESS'] = header['ADDRESS'].strip()

    for chapter in params['CHAPTERS']:
        chapter['TITLE'] = chapter['TITLE'].strip()

        for section in chapter['SECTIONS']:
            section['SUBTITLE'] = section['SUBTITLE'].strip()
            section['CONTENT'] = section['CONTENT'].strip()
            section['IMAGE_PATH'] = section['IMAGE_PATH'].strip()

    return params


def run():
    wasdi.wasdiLog("PDF tutorial v.1.1")

    # Read from the parameters file
    try:
        aoParams = wasdi.getParametersDict()
        aoParams = validateParameters(aoParams)
        aoParams = sanitizeParameters(aoParams)

        createPdf(aoParams['PDF_PATH'], aoParams)
    except Exception as oEx:
        wasdi.wasdiLog(f'An error occurred: {repr(oEx)}')
        wasdi.updateStatus("ERROR", 0)
        return


if __name__ == '__main__':
    wasdi.init("./config.json")
    run()
