import os
import uuid

import wasdi

from CustomPDF import CustomPDF


def create_pdf(pdf_path, params):
    pdf = CustomPDF(params)

    wasdi.wasdiLog("Creating PDF...")

    # Add the coverpage before adding chapters
    pdf.add_cover_page()
    # Add the index before adding chapters
    pdf.add_index()

    for i, chapter in enumerate(params['chapters'], start=1):
        pdf.print_chapter(i, chapter['title'], chapter)

    pdf.oversized_images = "WARN"
    pdf.output(pdf_path)

    wasdi.wasdiLog("PDF created successfully")


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



def validate_pdf_spec(pdf_spec):
    valid = True

    # Validate filename
    sFileName = pdf_spec.get("filename", "")
    if sFileName == "":
        sFileName = uuid.uuid4()
        print(f"FileName is not set! Generating a random UUID one... {sFileName}")
    elif os.path.splitext(sFileName)[1] != ".pdf":
        print("Filename does not have a '.pdf' extension.")
        valid = False

    # Validate cover_page
    cover_page = pdf_spec.get("cover_page", {})
    if not cover_page.get("template_image_filename"):
        print("Cover page template_image_filename is missing.")
        valid = False

    # Validate header
    header = pdf_spec.get("header", {})
    if not all(header.get(k) for k in ["title", "logo", "author_name", "company_name"]):
        print("Header is missing one or more required fields (title, logo, author_name, company_name).")
        valid = False

    # Validate chapters
    chapters = pdf_spec.get("chapters", [])
    if len(chapters) == 0:
        print("Chapters are empty.")
        valid = False

    for chapter in chapters:
        if not chapter.get("title"):
            print("One of the chapter titles is missing.")
            valid = False
        if not chapter.get("sections"):
            print(f"Chapter '{chapter.get('title')}' has no sections.")
            valid = False

    # Validate footer
    footer = pdf_spec.get("footer", {})
    if not all(footer.get(k) for k in ["company_link", "footer_link_alignment", "footer_page_number_alignment"]):
        print("Footer is missing one or more required fields.")
        valid = False

    # Validate style
    style = pdf_spec.get("style", {})
    if not all(style.get(k) for k in ["font_size", "font_family", "font_style", "title_background"]):
        print("Style is missing one or more required fields.")
        valid = False

    if valid:
        print("Validation passed.")
        return True
    else:
        print("Validation failed.")
        return False

def run():
    wasdi.wasdiLog("PDF tutorial v.1.4")

    # Reading the parameters
    # try:
    #
    #     aoParams = wasdi.getParametersDict()
    #     aoParams = sanitize_parameters(aoParams)
    #     # TODO check validation method
    #
    #     sFileName = aoParams["filename"]
    #
    #     if sFileName == "":
    #         sFileName = uuid.uuid4()
    #         wasdi.wasdiLog(f"FileName is not set! Generating a random UUID one... {sFileName}")
    #
    #     sFileName = f"{sFileName}.pdf"
    #     create_pdf(sFileName, aoParams)
    # except Exception as oEx:
    #     wasdi.wasdiLog(f'An error occurred: {repr(oEx)}')
    #     wasdi.updateStatus("ERROR", 0)
    #     return

    wasdi.wasdiLog("PDF tutorial v.1.4")
    aoParams = wasdi.getParametersDict()
    aoParams = sanitize_parameters(aoParams)

    sFileName = aoParams.get("filename", "")
    if sFileName == "":
        sFileName = str(uuid.uuid4()) + "report"
        wasdi.wasdiLog(f"FileName is not set! Generating a random UUID one... {sFileName}")
        aoParams["filename"] = sFileName  # Updating aoParams with the new filename

    is_valid = validate_pdf_spec(aoParams)  # Calling the validate function here

    if not is_valid:
        wasdi.wasdiLog("Validation failed. Exiting.")
        wasdi.updateStatus("ERROR", 0)
        return

    sFileName = f"{sFileName}.pdf" if not sFileName.endswith('.pdf') else sFileName
    create_pdf(sFileName, aoParams)

if __name__ == '__main__':
    wasdi.init("./config.json")
    run()
