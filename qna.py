
import os
import sys
import time
from typing import List

from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain_community.callbacks import get_openai_callback
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI, AzureChatOpenAI
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv

from utils.local_embeddings import embed  # NOQA
from utils.splitter import split_to_chunks  # NOQA


def qna(body: List[str] = [], doc_query: str = '', _save: bool = False) -> str:
    load_dotenv()
    input_docs = None
    if len(body) > 0:
        # llm = OpenAI()
        # Alternative llm:
        llm = AzureChatOpenAI(
            temperature=0,
            model="gpt-35-turbo-eastus-unfiltered",
            verbose=True,
            api_version=os.environ.get('BASE_VERSION'),
            azure_endpoint=os.environ.get('BASE'),
            openai_api_key=os.environ.get('BASE_KEY'),
            openai_api_type=os.environ.get('BASE_TYPE')
        )
        chain = load_qa_chain(llm, chain_type="stuff")
        # embeddings = OpenAIEmbeddings(disallowed_special=())
        embeddings = embed()

        if type(body[0]) is not str:
            body = split_to_chunks(body[0].page_content)
            print('> split body')

        print(type(body))
        print(len(body))
        start = time.time()

        local_path = './dump/3404'
        if os.path.exists(local_path) and _save:
            db = FAISS.load_local(local_path, embeddings)
            print('> local db is found at.', local_path)
            input_docs = db.similarity_search(doc_query, k=3)
            print(f'> SS Only: {(time.time() - start)} s')
        else:
            try:
                print('> starting FAISS...')
                db = FAISS.from_texts(body, embeddings)

                if _save:
                    print('> saving...')
                    db.save_local(local_path)

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
