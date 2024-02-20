
from typing import List
from langchain.docstore.document import Document
from langchain_community.document_loaders import UnstructuredMarkdownLoader

from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from utils.splitter import split_to_chunks  # NOQA


def load_documents(path: str = './pdf/src/', src_type: str = 'pdf') -> List[Document]:
    """
    Folder defaults to /pdf.\n
    Returns Document object to be split (into chunks). Document is a Langchain schema.
    """
    # TODO: add logic between different file types
    # loader = DirectoryLoader(
    #     path, glob=f'./*.{src_type}', loader_cls=UnstructuredMarkdownLoader)

    # Changed to single doc loader for now: 20 Feb 2024
    loader = TextLoader(path, 'utf-8', autodetect_encoding=True)
    docs = loader.load()
    print('> Found docs:', len(docs))
    return docs


if __name__ == '__main__':
    load_documents()
