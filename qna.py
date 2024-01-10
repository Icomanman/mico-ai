
import sys
import time
import streamlit as st
from typing import List

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.callbacks import get_openai_callback

from dotenv import load_dotenv

from utils.local_embeddings import embed  # NOQA


def qna(body: List[str] = [], doc_query: str = '') -> str:
    load_dotenv()
    input_docs = None
    if len(body) > 0:
        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type="stuff")
        # embeddings = OpenAIEmbeddings(disallowed_special=())
        embeddings = embed()
        start = time.time()

        try:
            db = FAISS.from_texts(body, embeddings)
            # Returns 'list' of Document object
            input_docs = db.similarity_search(doc_query, k=3)
            print(f'> embeddings + SS: {(time.time() - start)} s')
        except Exception as e:
            print(f'> qna:\n{e}')
            print(f'> embeddings ERROR: {(time.time() - start)} s')
            sys.exit(1)

    with get_openai_callback() as cb:
        start = time.time()
        response = chain.run(input_documents=input_docs, question=doc_query)
        print(f'> qna chain: {(time.time() - start)} s')
        print('\n> Result Callback:')
        print(cb)

    return response


if __name__ == '__main__':
    qna()
