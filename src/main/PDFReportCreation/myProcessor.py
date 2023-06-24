import json
import wasdi
import os
from fpdf import FPDF
from PIL import Image

class CustomPDF(FPDF):
    def __init__(self, params):
        super().__init__()
        self.asParametersDict = params

    def header(self):
        header_params = self.asParametersDict['header']
        title = header_params['title']
        logo = header_params['logo']
        name = header_params['name']
        company_name = header_params['company_name']
        address = header_params['address']

        # Set logo
        self.image(logo, x=10, y=10, w=30)

        # Set header title
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, title, border=0, ln=1, align='C')

        # Set name and company
        self.set_font('Helvetica', '', 12)
        self.cell(0, 5, '', ln=1, align='R')  # Empty cell for alignment
        self.cell(0, 5, f'Author: {name}', ln=1, align='R')
        self.cell(0, 5, f'Company: {company_name}', ln=1, align='R')
        self.cell(0, 5, f'Address: {address}', ln=1, align='R')
        self.ln(10)

    def footer(self):
        self.set_y(-10)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def chapter_title(self, ch_num, ch_title):
        self.set_fill_color(34, 139, 34)  # Set fill color to green
        self.set_text_color(255)  # Set text color to white
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, f'Chapter {ch_num}: {ch_title}', ln=1, fill=True)
        self.ln()

    def chapter_body(self, chapter_data):
        self.set_fill_color(255)  # Set fill color back to white
        self.set_text_color(0)  # Set text color back to black
        self.set_font('Times', '', 12)

        chapter_sections = chapter_data.get('sections', [])
        for section in chapter_sections:
            subtitle = section.get('subtitle')
            content = section.get('content')
            image_file = section.get('image_path')

            # Print subtitle
            self.set_font('Helvetica', 'B', 12)
            self.cell(0, 5, subtitle, ln=1, fill=True)
            self.ln()

            # Print content
            self.set_font('Times', '', 12)
            self.multi_cell(0, 10, content)
            self.ln(10)

            # Add image if specified
            if image_file:
                if os.path.exists(image_file):
                    # Calculate the available width for the image
                    available_width = self.w - self.l_margin - self.r_margin

                    # Load the image using PIL to get its dimensions
                    image = Image.open(image_file)
                    image_width, image_height = image.size

                    # Calculate the scale factor for resizing the image
                    scale_factor = available_width / image_width

                    # Calculate the scaled dimensions for the image
                    scaled_width = image_width * scale_factor
                    scaled_height = image_height * scale_factor

                    # Calculate the position to center the image vertically
                    image_y = self.get_y()

                    # Set the position for the image and print it
                    self.image(image_file, x=self.l_margin, y=image_y, w=scaled_width, h=scaled_height)
                else:
                    wasdi.wasdiLog(f"Image file not found: {image_file}")

    def print_chapter(self, ch_num, ch_title, chapter_data):
        self.add_page()
        self.chapter_title(ch_num, ch_title)
        self.chapter_body(chapter_data)


def create_pdf(pdf_path, params):
    pdf = CustomPDF(params)

    for key, value in params.items():
        wasdi.wasdiLog(f"{key}: {pdf.asParametersDict[key]}")

    pdf.set_author('Abdullah Al Foysal')

    pdf.add_page()

    for i, chapter in enumerate(params['chapters'], start=1):
        pdf.print_chapter(i, chapter['title'], chapter)

    pdf.output(pdf_path)


def validate_parameters(params):
    if 'pdf_path' not in params:
        wasdi.wasdiLog("Error: 'pdf_path' is missing in the parameters.")
        params['pdf_path'] = 'WASDI_FINAL_REPORT.pdf'  # Assign a default value
    else:
        if not params['pdf_path'].endswith('.pdf'):
            wasdi.wasdiLog("Warning: 'pdf_path' should have a '.pdf' extension.")

    if 'header' not in params:
        wasdi.wasdiLog("Error: 'header' is missing in the parameters.")
        params['header'] = {}  # Assign an empty dictionary

    header = params['header']
    if 'title' not in header:
        wasdi.wasdiLog("Error: 'title' is missing in the header.")
        header['title'] = 'WASDI FINAL REPORT'  # Assign a default value

    if 'logo' not in header:
        wasdi.wasdiLog("Error: 'logo' is missing in the header.")
        header['logo'] = 'wasdi_logo.jpg'  # Assign a default value

    if 'name' not in header:
        wasdi.wasdiLog("Error: 'name' is missing in the header.")
        header['name'] = ''  # Assign an empty string

    if 'company_name' not in header:
        wasdi.wasdiLog("Error: 'company_name' is missing in the header.")
        header['company_name'] = ''  # Assign an empty string

    if 'address' not in header:
        wasdi.wasdiLog("Error: 'address' is missing in the header.")
        header['address'] = ''  # Assign an empty string

    if 'chapters' not in params:
        wasdi.wasdiLog("Error: 'chapters' is missing in the parameters.")
        params['chapters'] = []  # Assign an empty list

    for chapter in params['chapters']:
        if 'title' not in chapter:
            wasdi.wasdiLog("Error: 'title' is missing in a chapter.")
            chapter['title'] = ''  # Assign an empty string

        if 'sections' not in chapter:
            wasdi.wasdiLog("Error: 'sections' is missing in a chapter.")
            chapter['sections'] = []  # Assign an empty list

        for section in chapter['sections']:
            if 'subtitle' not in section:
                wasdi.wasdiLog("Error: 'subtitle' is missing in a section.")
                section['subtitle'] = ''  # Assign an empty string

            if 'content' not in section:
                wasdi.wasdiLog("Error: 'content' is missing in a section.")
                section['content'] = ''  # Assign an empty string

            if 'image_path' not in section:
                wasdi.wasdiLog("Error: 'image_path' is missing in a section.")
                section['image_path'] = ''  # Assign an empty string

    return params


def sanitize_parameters(params):
    params['pdf_path'] = params['pdf_path'].strip()  # Remove leading/trailing whitespace

    header = params['header']
    header['title'] = header['title'].strip()
    header['logo'] = header['logo'].strip()
    header['name'] = header['name'].strip()
    header['company_name'] = header['company_name'].strip()
    header['address'] = header['address'].strip()

    for chapter in params['chapters']:
        chapter['title'] = chapter['title'].strip()

        for section in chapter['sections']:
            section['subtitle'] = section['subtitle'].strip()
            section['content'] = section['content'].strip()
            section['image_path'] = section['image_path'].strip()

    return params


def run():
    wasdi.wasdiLog("PDF tutorial v.1.1")
    wasdi.wasdiLog("PDF tutorial v.1.1")

    with open('params.json', 'r') as params_file:
        params = json.load(params_file)
        wasdi.wasdiLog("Printing params:")
        wasdi.wasdiLog(json.dumps(params, indent=4))

    params = validate_parameters(params)
    params = sanitize_parameters(params)

    create_pdf(params['pdf_path'], params)


if __name__ == '__main__':
    wasdi.init("./config.json")
    run()
