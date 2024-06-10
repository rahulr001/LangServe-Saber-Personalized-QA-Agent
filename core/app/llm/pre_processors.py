from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100, chunk_overlap=20)
    return text_splitter.split_text(text)


