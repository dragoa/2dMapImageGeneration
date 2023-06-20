This repository contains a Python script that generates a PDF report based on the provided parameters. The script utilizes the fpdf library to create the PDF document and the PIL library to handle image insertion. The report structure and content are defined in a JSON file.

Installation
To run the PDF generator, follow these steps:
Install the required dependencies. You can use pip to install them:
*pip install fpdf Pillow wasdi
Place the params.json file in the root directory of the cloned repository. This file contains the parameters and content for the PDF report.
Execute the Python script:
*python pdf_generator.py
The script will generate the PDF report based on the provided parameters and save it as WASDI FINAL REPORT.pdf.
Usage
Customizing the Report
To customize the generated report, you can modify the params.json file. This file contains the following sections:

pdf_path: The output PDF file name.
header: Parameters related to the report header, including the title, source URL, logo file path, author's name, company name, and address.
chapters: An array of chapters. Each chapter has a title and an array of sections. Each section consists of a subtitle, content, and an optional image file path.
Feel free to modify the parameters to fit your desired report structure and content.

Adding Images
To add images to the report, provide the file path in the corresponding section of the params.json file. Make sure the image file exists in the specified location. The script will automatically resize and insert the images into the report.

Output
The generated PDF report will be saved as WASDI FINAL REPORT.pdf in the root directory of the repository.
