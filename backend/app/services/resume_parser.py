
import io
import re
import zipfile

import pymupdf
from docx import Document


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def clean_extracted_text(text):
    """Clean extracted text without removing meaningful line breaks."""

    text = text.replace("\x00", "")
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    cleaned_lines = []

    for line in text.split("\n"):
        line = re.sub(r"[ \t]+", " ", line).strip()

        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def extract_pdf_text(file_bytes):
    """Extract text from a PDF document."""

    try:
        with pymupdf.open(stream=file_bytes, filetype="pdf") as pdf:

            if pdf.is_encrypted:
                raise ValueError(
                    "Password-protected PDFs are not supported."
                )

            if len(pdf) > 30:
                raise ValueError(
                    "PDF contains too many pages. Maximum allowed is 30."
                )

            pages = []

            for page in pdf:
                pages.append(page.get_text("text"))

            extracted_text = "\n".join(pages)

            return extracted_text, len(pdf)

    except ValueError:
        raise

    except Exception as error:
        raise ValueError(
            "Unable to read this PDF. Please upload a valid PDF file."
        ) from error


def extract_docx_text(file_bytes):
    """Extract text from paragraphs and tables in a DOCX document."""

    try:
        document = Document(io.BytesIO(file_bytes))

        extracted_parts = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                extracted_parts.append(paragraph.text)

        for table in document.tables:

            for row in table.rows:
                row_text = [
                    cell.text.strip()
                    for cell in row.cells
                    if cell.text.strip()
                ]

                if row_text:
                    extracted_parts.append(" | ".join(row_text))

        return "\n".join(extracted_parts)

    except Exception as error:
        raise ValueError(
            "Unable to read this Word document. "
            "Please upload a valid DOCX file."
        ) from error


def parse_resume_file(filename, file_bytes):
    """Validate and extract text from an uploaded resume."""

    if not filename:
        raise ValueError("Please select a resume file.")

    if not file_bytes:
        raise ValueError("The uploaded file is empty.")

    if len(file_bytes) > MAX_FILE_SIZE:
        raise ValueError("File size must not exceed 10 MB.")

    extension = filename.lower().rsplit(".", 1)[-1]

    if extension == "pdf":

        if not file_bytes.startswith(b"%PDF"):
            raise ValueError("The uploaded file is not a valid PDF.")

        extracted_text, page_count = extract_pdf_text(file_bytes)
        file_type = "PDF"

    elif extension == "docx":

        if not zipfile.is_zipfile(io.BytesIO(file_bytes)):
            raise ValueError("The uploaded file is not a valid DOCX.")

        extracted_text = extract_docx_text(file_bytes)
        page_count = None
        file_type = "DOCX"

    else:
        raise ValueError(
            "Unsupported file format. Please upload a PDF or DOCX file."
        )

    extracted_text = clean_extracted_text(extracted_text)

    if len(extracted_text) < 50:
        raise ValueError(
            "Very little text was extracted. "
            "The PDF may be scanned or image-based. "
            "Please upload a text-based PDF or DOCX file."
        )

    return {
        "filename": filename,
        "file_type": file_type,
        "extracted_text": extracted_text,
        "total_characters": len(extracted_text),
        "total_words": len(extracted_text.split()),
        "total_lines": len(extracted_text.splitlines()),
        "total_pages": page_count
    }
