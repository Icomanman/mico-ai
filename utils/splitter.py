
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader


def split_to_chunks(txt):
    splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=1000,
        chunk_overlap=60,
        length_function=len
    )
    return splitter.split_text(txt)


def split(pdf=None, title=''):
    if pdf is None:
        raise ValueError('> Invalid PDF.')

    reader = PdfReader(pdf)
    file_name = title if title else 'reader'

    page_no = 1
    body = []
    with open(f'./dump/{file_name}.md', 'w+', encoding='utf-8') as f:
        for page in reader.pages:
            new_page = ''
            new_page += f'### *Page {page_no}* ###\n'

            page_txt = page.extract_text()

            new_page += page_txt.replace('?', '--')
            new_page += '\n\n---\n'

            f.write(new_page)
            page_no += 1

            body.extend(split_to_chunks(new_page))

    return body


if __name__ == '__main__':
    split()
