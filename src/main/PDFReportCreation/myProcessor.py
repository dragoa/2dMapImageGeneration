import json
import wasdi
import os
from fpdf import FPDF
from PIL import Image

class CustomPDF(FPDF):
    def __init__(self, params):
        super().__init__()
        self.asParametersDict = params
        self.index_added = False  # Initialize index_added attribute to False

    def header(self):
        header_params = self.asParametersDict['header']
        title = header_params['title']
        logo = header_params['logo']
        name = header_params['name']
        company_name = header_params['company_name']
        address = header_params['address']
        website = header_params.get('website', '')  # Using get method to ensure backward compatibility
        telephone = header_params.get('telephone', '')

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
        self.cell(0, 5, f'Website: {website}', ln=1, align='R')
        self.cell(0, 5, f'Telephone: {telephone}', ln=1, align='R')
        self.ln(10)

    # Moved the add_index method out of the header
    def add_index(self):
        if not self.index_added:
            self.set_xy(10, 70)
            self.set_font('Helvetica', 'B', 16)
            self.set_text_color(255, 255, 255)
            self.cell(0, 10, 'INDEX', ln=1, align='L', fill=True)
            self.set_fill_color(255, 0, 0)
            self.set_text_color(0, 0, 0)
            self.set_font('Helvetica', '', 12)
            self.multi_cell(0, 10, self.generate_index(), align='L')
            self.index_added = True
            self.ln(10)

    # Moved the generate_index method out of the header
    def generate_index(self):
        index_text = ''
        for i, chapter in enumerate(self.asParametersDict['chapters'], start=1):
            index_text += f'Chapter {i}: {chapter["title"]}\n'
        return index_text

    def footer(self):
        self.set_y(-15)  # Position at 1.5 cm from bottom
        self.set_font('Arial', 'I', 8)
        page_number_alignment = self.asParametersDict.get('footer_page_number_alignment',
                                                          'center')  # Get page number alignment preference
        self.cell(0, 10, f'Page {self.page_no()}', align=page_number_alignment)

        company_link = self.asParametersDict['header'].get('company_link', '')  # Get company link from parameters
        if company_link:  # If a link is provided, add it to the footer
            link_alignment = self.asParametersDict.get('footer_link_alignment',
                                                       'center')  # Get link alignment preference
            link_x, link_y = self.calculate_link_position(link_alignment)

            self.set_xy(link_x, link_y)  # Position the cell for the link
            self.set_text_color(0, 0, 255)  # Set link color to blue
            self.set_font('Arial', 'U', 8)  # Set font to underline
            self.cell(0, 10, 'Wasdi', ln=True, align=link_alignment,
                      link=company_link)  # Add the link with anchor text
            self.set_text_color(0, 0, 0)  # Reset text color to black

    def chapter_title(self, ch_num, ch_title):
        self.set_fill_color(255, 0, 0)  # Set fill color to red
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
            image_x = section.get('image_x', self.l_margin)  # Default to left margin
            image_y = section.get('image_y', self.get_y())  # Default to current Y position
            image_width = section.get('image_width', available_width)
            image_height = section.get('image_height', available_height)

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
                    # Calculate the available width and height for the image
                    available_width = self.w - self.l_margin - self.r_margin
                    available_height = 30 * self.k  # Convert inches to points

                    # Load the image using PIL to get its dimensions
                    image = Image.open(image_file)
                    image_width, image_height = image.size

                    # Calculate the scale factor for resizing the image
                    scale_factor = min(available_width / image_width, available_height / image_height)

                    # Calculate the scaled dimensions for the image
                    scaled_width = image_width * scale_factor
                    scaled_height = image_height * scale_factor

                    # Calculate the position to center the image horizontally
                    image_x = self.l_margin + (available_width - scaled_width) / 2

                    # Calculate the position to center the image vertically
                    image_y = self.get_y()

                    # Set the position for the image and print it with the specified width and height
                    self.image(image_file, x=image_x, y=image_y, w=image_width, h=image_height)
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
    pdf.add_index()  # Add the index before adding chapters

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

    # Validate company details
    if 'company_address' not in header['header']:  # Corrected key access
        wasdi.wasdiLog("Warning: 'company_address' is missing in the header.")
        header['header']['company_address'] = ''  # Assign an empty string

    if 'company_link' not in header['header']:  # Corrected key access
        wasdi.wasdiLog("Warning: 'company_link' is missing in the header.")
        header['header']['company_link'] = ''  # Assign an empty string

    if 'company_phone' not in header['header']:  # Corrected key access
        wasdi.wasdiLog("Warning: 'company_phone' is missing in the header.")
        header['header']['company_phone'] = ''  # Assign an empty string

    if 'footer_link_alignment' not in header:
        wasdi.wasdiLog("Warning: 'footer_link_alignment' is missing in the header.")
        wasdi.wasdiLog("Using default alignment: 'center'")
        header['footer_link_alignment'] = 'center'  # Assign a default value

    if 'footer_page_number_alignment' not in header:
        wasdi.wasdiLog("Warning: 'footer_page_number_alignment' is missing in the header.")
        wasdi.wasdiLog("Using default alignment: 'center'")
        header['footer_page_number_alignment'] = 'center'  # Assign a default value

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


def get_user_image_params():
    image_x = float(input("Enter X-coordinate for image position: "))
    image_y = float(input("Enter Y-coordinate for image position: "))
    image_width = float(input("Enter image width: "))
    image_height = float(input("Enter image height: "))
    return image_x, image_y, image_width, image_height

def run():
    wasdi.wasdiLog("PDF tutorial v.1.1")

    try:
        aoParams = wasdi.getParametersDict()
        aoParams = validate_parameters(aoParams)
        aoParams = sanitize_parameters(aoParams)

        for chapter in aoParams['chapters']:
            for section in chapter['sections']:
                image_x, image_y, image_width, image_height = get_user_image_params()
                section['image_x'] = image_x
                section['image_y'] = image_y
                section['image_width'] = image_width
                section['image_height'] = image_height

        create_pdf(aoParams['pdf_path'], aoParams)
    except Exception as oEx:
        wasdi.wasdiLog(f'An error occurred: {repr(oEx)}')
        wasdi.updateStatus("ERROR", 0)
        return

if __name__ == '__main__':
    wasdi.init("./config.json")
    run()
