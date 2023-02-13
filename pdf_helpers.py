import fitz
import base64
import streamlit as st

def displayPDF(fileBytes, container = None, page = 1):
    if container is not None:
        container.empty()
    # Opening file from file path
    base64_pdf = base64.b64encode(fileBytes).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}#page{page}&zoom=85&toolbar=0&navpanes=0&scrollbar=0" width="700" height="1000" type="application/pdf"></iframe>'

    # Displaying File
    container = st.empty()
    with container.container():
        st.markdown(pdf_display, unsafe_allow_html=True)
    return container

def highlight_pdf(file, search_text):
    doc = fitz.open(stream=file, filetype="pdf")
    for page in doc:
        areas = page.search_for(search_text)
        for area in areas:
            highlight = page.add_highlight_annot(area)
    return doc.write()

def delete_highlights(fileBytes):
    doc = fitz.open(stream=fileBytes, filetype="pdf")
    for page in doc:
        annotations = page.annots()
        for annotation in annotations:
            r = page.delete_annot(annotation)
            print(r)
    return doc.write()

def get_all_text(fileBytes):
    doc = fitz.open(stream=fileBytes, filetype="pdf")
    text = []
    for page in doc:
        text.append(page.get_text())
    return "\n\n".join(text)