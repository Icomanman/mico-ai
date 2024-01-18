
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
    loader = DirectoryLoader(
        path, glob=f'./*.{src_type}', loader_cls=UnstructuredMarkdownLoader)
    docs = loader.load()
    return docs


if __name__ == '__main__':
    load_documents()
