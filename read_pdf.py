from PyPDF2 import PdfFileReader

def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    txt = f"""
    Information about {pdf_path}: 

    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of pages: {number_of_pages}
    """

    # creating a page object
    pageObj = pdf.getPage(0)

    # extracting text from page
    print(pageObj.extractText())
    print(txt)
    return information

if __name__ == '__main__':
    path = 'AWS.pdf'
    extract_information(path)