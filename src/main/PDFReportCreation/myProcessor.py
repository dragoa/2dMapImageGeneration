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


def validate_parameters(aoParams):
    # validation of the parameters
    sFileName = aoParams.get("filename", "")
    if sFileName == "":
        sFileName = str(uuid.uuid4()) + "report"
        wasdi.wasdiLog(f"FileName is not set! Generating a random UUID one... {sFileName}")
        aoParams["filename"] = sFileName  # Updating aoParams with the new filename

    sFileName = f"{sFileName}.pdf" if not sFileName.endswith('.pdf') else sFileName

    # Validate cover_page
    cover_page = aoParams.get("cover_page", {})
    if not cover_page.get("template_image_filename"):
        wasdi.wasdiLog("Cover page template_image_filename is missing.")

    # Validate header
    header = aoParams.get("header", {})
    if not all(header.get(k) for k in ["title", "logo", "author_name", "company_name"]):
        wasdi.wasdiLog("Header is missing one or more required fields (title, logo, author_name, company_name).")

    # Validate chapters
    chapters = aoParams.get("chapters", [])
    if len(chapters) == 0:
        wasdi.wasdiLog("Chapters are empty")

    # Validate footer
    footer = aoParams.get("footer", {})
    if not all(footer.get(k) for k in ["company_link", "footer_link_alignment", "footer_page_number_alignment"]):
        wasdi.wasdiLog("Footer is missing one or more required fields.")

    return sFileName


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
    sFileName = validate_parameters(aoParams)

    create_pdf(sFileName, aoParams)


if __name__ == '__main__':
    wasdi.init("./config.json")
    run()
