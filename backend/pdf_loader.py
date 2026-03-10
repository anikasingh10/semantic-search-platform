import re

from pypdf import PdfReader


def clean_text(text: str) -> str:
    """Normalize extracted PDF text.

    - Replace newlines with spaces
    - Remove common bullet/dash characters
    - Collapse repeated whitespace
    - Trim leading/trailing whitespace
    """

    if not text:
        return ""

    # Keep word hyphenation while removing common list/bullet markers.
    text = text.replace("\n", " ")

    # Remove bullet characters and list markers (e.g., "•", "–", "-" when used as list prefixes).
    text = re.sub(r"(?:(?<=\s)|^)[–—•·-]+(?=\s)", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text


def extract_text_from_pdf(file_path: str):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text