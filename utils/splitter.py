
import uuid
from typing import List
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader

from streamlit.runtime.uploaded_file_manager import UploadedFile


def split_to_chunks(txt: str) -> List[str]:
    splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=1000,
        chunk_overlap=60,
        length_function=len
    )
    return splitter.split_text(txt)


def split_pdf(pdf: UploadedFile = None, title: str = '') -> List[str]:
    if pdf is None:
        raise ValueError('> Invalid PDF.')

    reader = PdfReader(pdf)
    file_name = title if title else f'user-file-{uuid.uuid4()}'

    page_no = 1
    body = ''
    with open(f'./dump/{file_name}.md', 'w+', encoding='utf-8') as f:
        for page in reader.pages:
            new_page = ''
            new_page += f'### *Page {page_no}* ###\n'

            page_txt = page.extract_text()

            new_page += page_txt.replace('?', '--')
            new_page += '\n\n---\n'

            f.write(new_page)
            page_no += 1

            body += new_page

    return split_to_chunks(body)


if __name__ == '__main__':
    split_pdf()
