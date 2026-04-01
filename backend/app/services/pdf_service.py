import asyncio
from io import BytesIO

import fitz


def _extract_pdf_pages(content: bytes) -> list[dict]:
    pages: list[dict] = []
    doc = fitz.open(stream=content, filetype='pdf')
    try:
        for i, page in enumerate(doc):
            text = page.get_text('text').strip()
            if text:
                pages.append({'page_number': i + 1, 'text': text})
    finally:
        doc.close()
    return pages


async def extract_pdf_pages_async(content: bytes) -> list[dict]:
    return await asyncio.to_thread(_extract_pdf_pages, content)


async def read_upload_file(upload_file) -> bytes:
    data = await upload_file.read()
    return BytesIO(data).getvalue()
