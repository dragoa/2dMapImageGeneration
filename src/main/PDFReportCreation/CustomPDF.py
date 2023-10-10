import os
import wasdi
from PIL import Image
from fpdf import FPDF


class CustomPDF(FPDF):
    """
    Custom class for creating a PDF using the fpdf library
    """

    def __init__(self, params):
        super().__init__()
        self.asParametersDict = params
        self.oCoverPage = params.get("cover_page")
        self.oHeader = params.get("header")
        self.oStyle = self.asParametersDict.get("style", {})  # Providing a default empty dict
        self.index_added = False  # No index present
        self.cover_added = False  # No cover page present

    # Add cover page method
    def add_cover_page(self):
        """
        Add a cover page to the PDF if it exists in the parameters.
        """
        if "cover_page" in self.asParametersDict:
            self.add_page()
            self.set_xy(10, 10)

            # Check if cover_page section has the template_image_filename attribute
            if "template_image_filename" in self.oCoverPage:
                coverpageFilename = self.oCoverPage["template_image_filename"]
                if os.path.exists(coverpageFilename):
                    self.image(coverpageFilename, x=10, y=self.get_y(), w=190)
                    self.ln(200)  # Move below the image, adjust as per image height
            else:
                # No cover page provided, do nothing
                pass

            self.cover_added = True  # Set cover_added to True
            self.add_page()

    # Modify the header function
    def header(self):
        """
        Define the PDF header with style based on JSON parameters.
        """
        if "header" in self.asParametersDict:
            if self.cover_added:
                header_params = self.asParametersDict["header"]

                # Extract title information
                title_info = header_params.get("title", {})
                title_text = title_info.get("text", "")
                title_style = title_info.get("style", {})
                title_font_size = title_style.get("font_size", 12)
                title_font_family = title_style.get("font_family", "Arial")
                title_font_style = title_style.get("font_style", "")
                title_text_color = title_style.get("text_color", [0, 0, 0])
                title_text_alignment = title_style.get("text_alignment", "C")

                # Apply style to title
                self.set_font(title_font_family, title_font_style, title_font_size)
                self.set_text_color(*title_text_color)
                self.cell(0, 10, title_text, border=0, ln=1, align=title_text_alignment)

                # Extract logo information and position
                logo_info = header_params.get("logo", {})
                logo_filename = logo_info.get("image_filename", "")
                logo_position = logo_info.get("position", {})
                logo_x = logo_position.get("x", 10)
                logo_y = logo_position.get("y", 10)
                logo_width = logo_position.get("w", 30)

                # Insert logo at specified position
                if logo_filename and os.path.exists(logo_filename):
                    self.image(logo_filename, x=logo_x, y=logo_y, w=logo_width)

                # Extract and display other header information
                self.set_font("Arial", "", 12)
                self.set_text_color(0, 0, 0)

                # Apply style for author information
                author_style = header_params.get("style", {})
                author_font_size = author_style.get("font_size", 12)
                author_font_family = author_style.get("font_family", "Arial")
                author_font_style = author_style.get("font_style", "")
                author_text_color = author_style.get("text_color", [0, 0, 0])
                author_text_alignment = author_style.get("text_alignment", "C")

                self.set_font(author_font_family, author_font_style, author_font_size)
                self.set_text_color(*author_text_color)

                self.cell(0, 5, f"Author: {header_params.get('author_name', '')}", ln=1, align=author_text_alignment)
                self.cell(0, 5, f"Company: {header_params.get('company_name', '')}", ln=1, align=author_text_alignment)
                self.cell(0, 5, f"Address: {header_params.get('address', '')}", ln=1, align=author_text_alignment)
                self.cell(0, 5, f"Website: {header_params.get('website', '')}", ln=1, align=author_text_alignment)
                self.cell(0, 5, f"Telephone: {header_params.get('telephone', '')}", ln=1, align=author_text_alignment)

                self.ln(10)

    def add_index(self):
        """
        Add an index to the PDF.
        """
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
        """
        Generate the index content for the PDF.
        """
        index_text = ""
        for i, chapter in enumerate(self.asParametersDict["chapters"], start=1):
            index_text += f'Chapter {i}: {chapter["title"]}\n'
        return index_text

    def footer(self):
        """
        Define the PDF footer.
        """
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
        """
        Define the title for a chapter in the PDF.
        """
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

    def fit_image(self, img_path, x, y, w, h):
        """
        Fit an image within a bounding box, keeping aspect ratio and centering it.
        """
        with Image.open(img_path) as img:
            aspect_ratio = img.width / img.height
            if aspect_ratio > 1:
                new_w = w
                new_h = w / aspect_ratio
                if new_h > h:
                    new_h = h
                    new_w = h * aspect_ratio
            else:
                new_h = h
                new_w = h * aspect_ratio
                if new_w > w:
                    new_w = w
                    new_h = w / aspect_ratio

            # Calculate the centered x and y positions
            x_centered = (w - new_w) / 2
            y_centered = (h - new_h) / 2

            self.image(img_path, x=x + x_centered, y=y + y_centered, w=new_w, h=new_h)

    def chapter_body(self, chapter_data):
        """
        Define the body content for a chapter in the PDF.
        """
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

            # Capture the Y position before the image to make sure it doesn't overlap with text or table
            y_position_before_image = self.get_y()

            # Handle image placement
            image_file = section.get("image_path", "")
            image_x_raw = section.get("image_x")
            image_y_raw = section.get("image_y")
            image_width = float(section.get("image_width", 100))
            image_height = float(section.get("image_height", 100))

            # If image_x and image_y are empty or not specified, set them to center the image
            if not image_x_raw and not image_y_raw:
                image_x = (self.w - image_width) / 2  # Center horizontally
                image_y = (self.h - image_height) / 2  # Center vertically
            else:
                image_x = float(image_x_raw) if image_x_raw else 0
                image_y = float(image_y_raw) if image_y_raw else 0

            self.set_font('Helvetica', 'B', 12)
            self.cell(0, 5, subtitle, ln=1, fill=True)
            self.ln(10)

            self.set_font('Times', '', 12)
            self.multi_cell(0, 10, content)
            self.set_y(self.get_y() + 10)

            # Add the image
            if image_file and os.path.exists(image_file):
                try:
                    self.fit_image(image_file, x=image_x, y=image_y, w=image_width, h=image_height)
                    self.set_y(image_y + image_height + 10)  # Explicitly set Y position for the text below the image
                except Exception as e:
                    wasdi.wasdiLog(f"An error occurred while processing the image '{image_file}'. {str(e)}")
            else:
                wasdi.wasdiLog(f"Image file not found or not specified: {image_file}")

    def add_table(self, data, col_widths, x=None, y=None):
        """
        Add a table to the PDF.
        """
        if x is not None and y is not None:
            self.set_xy(x, y)

        row_height = 10  # Adjust this value as needed for the desired row height

        for row in data:
            for i, col in enumerate(row):
                self.cell(col_widths[i], row_height, str(col), border=1)
            self.ln()  # Move to the next line (row)
            y += row_height  # Update the y position for the next row
            self.set_xy(x, y)  # Set the position for the next row

    def print_chapter(self, ch_num, ch_title, chapter_data):
        """
        Print a chapter in the PDF.
        """
        self.add_page()
        self.chapter_title(ch_num, ch_title)
        self.chapter_body(chapter_data)

        # Print table(s) if present
        tables = chapter_data.get('tables', [])
        for table in tables:
            if 'data' in table and 'col_widths' in table:
                table_data = table['data']
                col_widths = table['col_widths']

                # Extract the position and dimensions from the JSON data
                x_position = table.get('table_x', 0)  # Default to 0 if not specified
                y_position = table.get('table_y', 0)  # Default to 0 if not specified

                self.add_table(table_data, col_widths, x=x_position, y=y_position)
