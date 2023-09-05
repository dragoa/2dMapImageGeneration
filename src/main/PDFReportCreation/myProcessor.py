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

    aoParams = wasdi.getParametersDict()
    aoParams = sanitize_parameters(aoParams)
    # TODO check validation method

    sFileName = aoParams["filename"]

    if sFileName == "":
        sFileName = uuid.uuid4()
        wasdi.wasdiLog(f"FileName is not set! Generating a random UUID one... {sFileName}")

    sFileName = f"{sFileName}.pdf"
    create_pdf(sFileName, aoParams)


if __name__ == '__main__':
    wasdi.init("./config.json")
    run()
