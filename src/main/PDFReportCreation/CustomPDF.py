import os

import wasdi
from PIL import Image
from fpdf import FPDF


class CustomPDF(FPDF):
    def __init__(self, params):
        super().__init__()
        self.asParametersDict = params
        self.index_added = False  # Initialize index_added attribute to False
        self.style = self.asParametersDict.get("style")

    def header(self):
        header_params = self.asParametersDict["header"]
        title = header_params["title"]
        logo = header_params["logo"]
        name = header_params["name"]
        company_name = header_params["company_name"]
        address = header_params["address"]
        website = header_params.get("website", "")  # Using get method to ensure backward compatibility
        telephone = header_params.get("telephone", "")

        # Set up the logo
        self.image(logo, x=10, y=10, w=30)

        # Set header title
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, title, border=0, ln=1, align='C')

        # Set name and company
        try:
            self.set_font(self.style["family"], self.style["style"], self.style["size"])
        except Exception as oEx:
            self.set_font('Arial', '', 12)
            wasdi.wasdiLog(f'An error occurred setting up the style: {repr(oEx)}')

        self.cell(0, 5, '', ln=1, align='R')  # Empty cell for alignment
        self.cell(0, 5, f'Author: {name}', ln=1, align='R')
        self.cell(0, 5, f'Company: {company_name}', ln=1, align='R')
        self.cell(0, 5, f'Address: {address}', ln=1, align='R')
        self.cell(0, 5, f'Website: {website}', ln=1, align='R')
        self.cell(0, 5, f'Telephone: {telephone}', ln=1, align='R')
        self.ln(10)

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

    def generate_index(self):
        index_text = ''
        for i, chapter in enumerate(self.asParametersDict['chapters'], start=1):
            index_text += f'Chapter {i}: {chapter["title"]}\n'
        return index_text

    def footer(self):
        self.set_y(-15)  # Position at 1.5 cm from bottom
        self.set_font('Arial', 'I', 10)
        page_number_alignment = self.asParametersDict.get('footer_page_number_alignment', 'C')
        self.cell(0, 10, f'Page {self.page_no()}', align=page_number_alignment)

        header_params = self.asParametersDict['footer']
        company_link = header_params.get('company_link', '')
        footer_link_alignment = header_params.get('footer_link_alignment', 'C')

        if company_link:
            self.set_xy(10, -10)  # Adjust the position based on alignment
            self.set_text_color(0, 0, 255)
            self.set_font('Arial', 'U', 10)
            self.cell(0, 10, 'Wasdi', ln=True, align=footer_link_alignment, link=company_link)
            self.set_text_color(0, 0, 0)

    def chapter_title(self, ch_num, ch_title):
        self.set_fill_color(255, 0, 0)  # Set fill color to red
        self.set_text_color(255)  # Set text color to white
        self.set_font('Helvetica', 'B', 13)
        self.cell(0, 10, f'Chapter {ch_num}: {ch_title}', ln=1, fill=True)
        self.ln()

    def chapter_body(self, chapter_data):
        self.set_fill_color(255)  # Set fill color back to white
        self.set_text_color(0)  # Set text color back to black

        try:
            self.set_font(self.style["family"], self.style["style"], self.style["size"])
        except Exception as oEx:
            self.set_font('Arial', '', 12)
            wasdi.wasdiLog(f'An error occurred setting up the style: {repr(oEx)}')

        chapter_sections = chapter_data.get('sections', [])
        for section in chapter_sections:
            subtitle = section.get("subtitle")
            content = section.get("content")
            image_file = section.get("image_path")
            image_x = section.get("image_x")
            image_y = section.get("image_x")
            image_width = section.get("image_width")
            image_height = section.get("image_height")

            # Print subtitle
            self.cell(0, 5, subtitle, ln=1, fill=True)
            self.ln()

            # Print content
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
                    if image_width and image_height == "":
                        image_width, image_height = image.size

                        # Calculate the scale factor for resizing the image
                        scale_factor = min(available_width / image_width, available_height / image_height)

                        # Calculate the scaled dimensions for the image
                        image_width = image_width * scale_factor
                        image_height = image_height * scale_factor

                        if image_x and image_y == "":
                            # Calculate the position to center the image horizontally
                            image_x = self.l_margin + (available_width - image_width) / 2
                            # Calculate the position to center the image vertically
                            image_y = self.get_y()

                    # Set the position for the image and print it
                    self.image(image_file, x=image_x, y=image_y, w=image_width, h=image_height)
                else:
                    wasdi.wasdiLog(f"Image file not found: {image_file}")

    def add_table(self, data, col_widths):
        for row in data:
            for i, col in enumerate(row):
                self.cell(col_widths[i], 10, str(col), border=1)
            self.ln()

    def print_chapter(self, ch_num, ch_title, chapter_data):
        self.add_page()
        self.chapter_title(ch_num, ch_title)
        self.chapter_body(chapter_data)

        # Print table(s) if present
        tables = chapter_data.get('tables', [])
        for table in tables:
            if 'data' in table and 'col_widths' in table:
                table_data = table['data']
                col_widths = table['col_widths']
                self.add_table(table_data, col_widths)
