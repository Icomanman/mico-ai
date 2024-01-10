
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceBgeEmbeddings

hf_model = 'jinaai/jina-embedding-b-en-v1'
default_device = 'cpu'  # or 'cuda' if available


def embed():
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=hf_model, model_kwargs={'device': default_device})
    return embeddings
