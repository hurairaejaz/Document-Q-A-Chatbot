import fitz
def extract_text_from_pdf(pdf_path):
    """
    Extract text page by page.
    """
    pages = []
    doc = fitz.open(pdf_path)
    for page_number, page in enumerate(doc):
        text = page.get_text()
        if text.strip():
            pages.append(
                {
                    "page": page_number + 1,
                    "text": text
                }
            )
    doc.close()
    return pages