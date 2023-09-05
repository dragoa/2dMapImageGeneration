import os

import wasdi
from PIL import Image
from fpdf import FPDF


class CustomPDF(FPDF):
    """
    Custom class for creating a PDF using fpdf library
    """
    def __init__(self, params):

        super().__init__()
        self.asParametersDict = params
        self.oCoverPage = params.get("cover_page")
        self.oHeader = params.get("header")
        self.oStyle = self.asParametersDict.get("style")
        self.index_added = False  # No index present
        self.cover_added = False  # No coverpage present

    # Add cover page method
    def add_cover_page(self):

        self.add_page()
        self.set_xy(10, 10)

        # Image (if applicable)
        coverpageFilename = self.oCoverPage.get("template_image_filename", "")
        if coverpageFilename and os.path.exists(coverpageFilename):
            self.image(coverpageFilename, x=10, y=self.get_y(), w=190)
            self.ln(200)  # Move below the image, adjust as per image height
        else:
            # Title
            self.set_font('Helvetica', 'B', 20)
            self.cell(0, 20, self.oHeader.get("title", "Cover Page"), ln=1, align='C')
            self.ln(20)
        self.cover_added = True  # Set cover_added to True
        self.add_page()

    def header(self):

        if self.cover_added:  # Check if this is the cover page
            title = self.oHeader["title"]
            logo = self.oHeader["logo"]
            author_name = self.oHeader["author_name"]
            company_name = self.oHeader["company_name"]
            address = self.oHeader.get("address", "")
            website = self.oHeader.get("website", "")
            telephone = self.oHeader.get("telephone", "")

            # Set up the logo
            self.image(logo, x=10, y=10, w=30)

            # Set header title
            self.set_font("Helvetica", "B", 15)
            self.cell(0, 10, title, border=0, ln=1, align="C")

            # Set name and company
            try:
                self.set_font(self.oStyle["font_family"], self.oStyle["font_style"], self.oStyle["font_size"])
            except Exception as oEx:
                self.set_font("Arial", "", 12)
                wasdi.wasdiLog(f"An error occurred setting up the style: {repr(oEx)}")

            self.cell(0, 5, "", ln=1, align="R")  # Empty cell for alignment
            self.cell(0, 5, f"Author: {author_name}", ln=1, align="R")
            self.cell(0, 5, f"Company: {company_name}", ln=1, align="R")
            self.cell(0, 5, f"Address: {address}", ln=1, align="R")
            self.cell(0, 5, f"Website: {website}", ln=1, align="R")
            self.cell(0, 5, f"Telephone: {telephone}", ln=1, align="R")
            self.ln(10)

    def add_index(self):

        if not self.index_added:
            # Extract the title_background color from the style dictionary.
            # If it is not found, use black (#000000) as the default color.
            title_background = self.oStyle.get("title_background", "#000000")

            # Convert the hexadecimal color to an RGB tuple.
            hex_color = title_background.lstrip("#")
            rgb_tuple = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
            red, green, blue = rgb_tuple

            # Set up the index title and background color.
            self.set_xy(10, 70)
            self.set_font("Helvetica", "B", 16)
            self.set_text_color(255, 255, 255)  # Set text color to white
            self.set_fill_color(red, green, blue)  # Set fill color based on user's choice or default to black
            self.cell(0, 10, "INDEX", ln=1, align="L", fill=True)

            # Reset text color and fill color for the rest of the index.
            self.set_text_color(0, 0, 0)  # Set text color back to black
            self.set_fill_color(255, 255, 255)  # Set fill color back to white
            self.set_font("Helvetica", "", 12)
            self.multi_cell(0, 10, self.generate_index(), align="L")

            self.index_added = True
            self.ln(10)

    def generate_index(self):

        index_text = ""
        for i, chapter in enumerate(self.asParametersDict["chapters"], start=1):
            index_text += f'Chapter {i}: {chapter["title"]}\n'
        return index_text

    def footer(self):

        self.set_y(-15)  # Position at 1.5 cm from bottom
        self.set_font("Arial", "I", 10)
        page_number_alignment = self.asParametersDict.get("footer_page_number_alignment", "C")
        self.cell(0, 10, f"Page {self.page_no()}", align=page_number_alignment)

        header_params = self.asParametersDict["footer"]
        company_link = header_params.get("company_link", "")
        footer_link_alignment = header_params.get("footer_link_alignment", "C")

        if company_link:
            self.set_xy(10, -10)  # Adjust the position based on alignment
            self.set_text_color(0, 0, 255)
            self.set_font("Arial", "U", 10)
            self.cell(0, 10, "Wasdi", ln=True, align=footer_link_alignment, link=company_link)
            self.set_text_color(0, 0, 0)

    def chapter_title(self, ch_num, ch_title):

        # Extract the title_background color from the style dictionary.
        # If it is not found, use black (#000000) as the default color.
        title_background = self.oStyle.get("title_background", "#000000")

        # Convert the hexadecimal color to an RGB tuple.
        hex_color = title_background.lstrip("#")
        rgb_tuple = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        red, green, blue = rgb_tuple

        self.set_fill_color(red, green, blue)  # Set fill color to red
        self.set_text_color(255)  # Set text color to white
        self.set_font('Helvetica', 'B', 13)
        self.cell(0, 10, f'Chapter {ch_num}: {ch_title}', ln=1, fill=True)
        self.ln()

    def fit_image(self, img_path, x=None, y=None, w=None, h=None):
        """Fit the image within the bounding box, keeping aspect ratio."""

        # If any parameter is None, set it to None, otherwise convert it to float
        x = None if x is None else float(x)
        y = None if y is None else float(y)
        w = None if w is None else float(w)
        h = None if h is None else float(h)
        with Image.open(img_path) as img:
            aspect_ratio = img.width / img.height
            max_width = 190  # Set this according to your PDF dimensions
            max_height = 200  # Set this according to your PDF dimensions

            # If width and height are explicitly given, use them; otherwise, calculate
            new_w = w if w else max_width
            new_h = h if h else (new_w / aspect_ratio)

            if not w and not h:
                if aspect_ratio > 1:
                    new_w = max_width
                    new_h = new_w / aspect_ratio
                    if new_h > max_height:
                        new_h = max_height
                        new_w = new_h * aspect_ratio
                else:
                    new_h = max_height
                    new_w = new_h * aspect_ratio
                    if new_w > max_width:
                        new_w = max_width
                        new_h = new_w / aspect_ratio

            x = x if x is not None else (max_width - new_w) / 2
            y = y if y is not None else self.get_y()

            # Add the image to PDF
            self.image(img_path, x=x, y=y, w=new_w, h=new_h)

    def chapter_body(self, chapter_data):

        self.set_fill_color(255)  # Set fill color back to white
        self.set_text_color(0)  # Set text color back to black

        try:
            self.set_font(self.oStyle["font_family"], self.oStyle["font_style"], self.oStyle["font_size"])
        except Exception as oEx:
            self.set_font('Arial', '', 12)
            wasdi.wasdiLog(f'An error occurred setting up the style: {repr(oEx)}')

        chapter_sections = chapter_data.get('sections', [])
        for section in chapter_sections:
            subtitle = section.get("subtitle", "Default Subtitle")
            content = section.get("content", "Default Content")

            image_file = section.get("image_path", "")
            image_x_raw = section.get("image_x")
            image_y_raw = section.get("image_y")
            image_width_raw = section.get("image_width")
            image_height_raw = section.get("image_height")

            image_x = 10 if not image_x_raw or image_x_raw in ["None", "none", ""] else float(image_x_raw)
            image_y = self.get_y() if not image_y_raw or image_y_raw in ["None", "none", ""] else float(image_y_raw)
            image_width = 100 if not image_width_raw or image_width_raw in ["None", "none", ""] else float(
                image_width_raw)
            image_height = 100 if not image_height_raw or image_height_raw in ["None", "none", ""] else float(
                image_height_raw)

            self.set_font('Helvetica', 'B', 12)
            self.cell(0, 5, subtitle, ln=1, fill=True)
            self.ln(10)

            self.set_font('Times', '', 12)
            self.multi_cell(0, 10, content)
            self.set_y(self.get_y() + 10)

            # Calculate Y position to start image
            start_y = self.get_y() + 10  # Assuming 10 units below the current text

            if image_file and os.path.exists(image_file):
                try:
                    self.fit_image(image_file, y=start_y, w=image_width, h=image_height)
                    self.set_y(start_y + image_height + 10)  # Move Y position below the image
                except Exception as e:
                    wasdi.wasdiLog(f"An error occurred while processing the image '{image_file}'. {str(e)}")
            else:
                wasdi.wasdiLog(f"Image file not found or not specified: {image_file}")

    def add_table(self, data, col_widths, table_x=None, table_y=None, table_width=None, table_height=None):
        count = 0

        # If x and y positions are specified, set them, else set to default values
        table_x = table_x if table_x is not None else 20
        table_y = table_y if table_y is not None else self.get_y()

        self.set_xy(table_x, table_y)

        for row in data:
            for i, col in enumerate(row):
                if table_width and table_height:
                    self.cell(table_width / len(row), table_height / len(data), str(col), border=1)
                else:
                    self.cell(col_widths[i], 10, str(col), border=1)
            self.ln()
            count += 1

        if table_height:
            self.set_y(self.get_y() + table_height)
        else:
            self.set_y(self.get_y() + 10 * count)

    def print_chapter(self, ch_num, ch_title, chapter_data):
        self.add_page()
        self.chapter_title(ch_num, ch_title)
        self.chapter_body(chapter_data)

        # Print table(s) if present
        # Print table(s) if present
        tables = chapter_data.get('tables', [])
        for table in tables:
            if 'data' in table and 'col_widths' in table:
                self.ln()

                # Capture the Y position before the table to make sure it doesn't overlap with text or image
                y_position_before_table = self.get_y()

                table_data = table['data']
                col_widths = table['col_widths']
                table_x = table.get('table_x', 20)  # Default is None if not set
                table_y = table.get('table_y', y_position_before_table)  # Default is None if not set
                table_width = table.get('table_width')  # Default is None if not set
                table_height = table.get('table_height')  # Default is None if not set

                self.add_table(table_data, col_widths, table_x, table_y, table_width, table_height)
