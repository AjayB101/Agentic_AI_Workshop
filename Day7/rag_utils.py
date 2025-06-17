import PyPDF2
import docx
import tempfile

def extract_text_from_file(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]:
        return extract_text_from_doc_or_txt(file)
    else:
        return ""

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

def extract_text_from_doc_or_txt(file):
    if file.type == "text/plain":
        return file.read().decode("utf-8")
    else:  # docx
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.read())
            doc = docx.Document(tmp.name)
            return "\n".join([p.text for p in doc.paragraphs])

def ask_question_over_text(llm, text, question):
    prompt = f"Context:\n{text}\n\nQuestion: {question}\nAnswer:"
    return llm.invoke(prompt) if hasattr(llm, "invoke") else llm(prompt)
