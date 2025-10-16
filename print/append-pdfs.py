#!/usr/bin/env python3

from pypdf import PdfReader, PdfWriter


def append_pdfs(input_pdf1, input_pdf2, output_pdf):
    """
    Append two PDF files together.

    Args:
        input_pdf1: Path to the first PDF file
        input_pdf2: Path to the second PDF file (will be appended)
        output_pdf: Path for the output merged PDF file
    """
    # Create a PDF writer object
    writer = PdfWriter()

    # Read and add pages from the first PDF
    reader1 = PdfReader(input_pdf1)
    for page in reader1.pages:
        writer.add_page(page)

    # Read and add pages from the second PDF
    reader2 = PdfReader(input_pdf2)
    for page in reader2.pages:
        writer.add_page(page)

    # Write the merged PDF to output file
    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)

    print(f'{input_pdf1} + {input_pdf2} --> {output_pdf}')


if __name__ == '__main__':
    import sys

    first_pdf, second_pdf, output_file = sys.argv[1:]

    try:
        append_pdfs(first_pdf, second_pdf, output_file)
    except FileNotFoundError as e:
        print(f'Error: Could not find PDF file - {e}')
    except Exception as e:
        print(f'Error: {e}')
