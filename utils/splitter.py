
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader


def split(pdf=None, title=''):
    if pdf is None:
        raise ValueError('> Invalid PDF.')

    reader = PdfReader(pdf)
    file_name = title if title else 'reader'

    page_no = 1
    body = ''
    with open(f'./dump/{file_name}.md', 'w+') as f:
        for page in reader.pages:
            body += f'### *Page {page_no}*\n'
            body += page.extract_text()
            body += '\n\n---\n'
            # f.write(f'### *Page {page_no}*\n')
            # f.write(page.extract_text())
            # f.write('\n\n---\n')
            f.write(body)
            page_no += 1
    return body


if __name__ == '__main__':
    split()
