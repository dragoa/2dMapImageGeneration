import wasdi

from CustomPDF import CustomPDF


def create_pdf(pdf_path, params):
    pdf = CustomPDF(params)

    wasdi.wasdiLog("Creating PDF...")

    for key, value in params.items():
        wasdi.wasdiLog(f"{key}: {pdf.asParametersDict[key]}")

    pdf.set_author('Abdullah Al Foysal')
    pdf.add_page()
    pdf.add_index()  # Add the index before adding chapters

    for i, chapter in enumerate(params['chapters'], start=1):
        pdf.print_chapter(i, chapter['title'], chapter)

    pdf.oversized_images = "WARN"
    pdf.output(pdf_path)

    wasdi.wasdiLog("PDF created successfully")


def get_user_image_params():
    image_x = float(input("Enter X-coordinate for image position: "))
    image_y = float(input("Enter Y-coordinate for image position: "))
    image_width = float(input("Enter image width: "))
    image_height = float(input("Enter image height: "))
    return image_x, image_y, image_width, image_height


def sanitize_parameters(params):
    # Recursive function that removes leading/trailing whitespace
    if isinstance(params, str):
        return params.strip()
    elif isinstance(params, list):
        return [sanitize_parameters(item) for item in params]
    elif isinstance(params, dict):
        return {key: sanitize_parameters(value) for key, value in params.items()}
    else:
        return params


def validate_parameters(params):
    if "filename" not in params:
        wasdi.wasdiLog("A filename is missing in the parameters! Using a default one")
        params["filename"] = "Wasdi report"  # Assign a default value

    if "header" not in params:
        wasdi.wasdiLog("Header is missing in the parameters.")
        params["header"] = {}  # Assign an empty dictionary

    header = params["header"]
    if "title" not in header:
        wasdi.wasdiLog("Title is missing in the header.")
        header['title'] = 'WASDI FINAL REPORT'  # Assign a default value

    if "logo" not in header:
        wasdi.wasdiLog("Logo is missing in the header.")
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
    if 'company_address' not in header:  # Corrected key access
        wasdi.wasdiLog("Warning: 'company_address' is missing in the header.")
        header['company_address'] = ''  # Assign an empty string

    if 'company_link' not in header:  # Corrected key access
        wasdi.wasdiLog("Warning: 'company_link' is missing in the header.")
        header['company_link'] = ''  # Assign an empty string

    if 'company_phone' not in header:  # Corrected key access
        wasdi.wasdiLog("Warning: 'company_phone' is missing in the header.")
        header['company_phone'] = ''  # Assign an empty string

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


def run():
    wasdi.wasdiLog("PDF tutorial v.1.2")

    # Reading the parameters
    try:

        aoParams = wasdi.getParametersDict()
        aoParams = sanitize_parameters(aoParams)
        aoParams = validate_parameters(aoParams)

        filename = f"{aoParams['filename']}.pdf"
        create_pdf(filename, aoParams)
    except Exception as oEx:
        wasdi.wasdiLog(f'An error occurred: {repr(oEx)}')
        wasdi.updateStatus("ERROR", 0)
        return


if __name__ == '__main__':
    wasdi.init("./config.json")
    run()
