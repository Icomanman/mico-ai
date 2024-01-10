
from typing import List
from langchain.docstore.document import Document
from langchain.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader

from splitter import split_to_chunks  # NOQA


def load_documents(path: str = './pdf/src/') -> List[Document]:
    """
    Folder defaults to /pdf.\n
    Returns Document object to be split (into chunks). Document is a Langchain schema.
    """

    loader = DirectoryLoader(path, glob='./*.pdf', loader_cls=PyPDFLoader)
    docs = loader.load()
    print(type(docs))
    return docs


if __name__ == '__main__':
    load_documents()
