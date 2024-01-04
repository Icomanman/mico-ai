
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

from app import retrieve_info  # NOQA
from dotenv import load_dotenv


def qna(doc_query='', body='') -> str:
    load_dotenv()
    llm = OpenAI()
    chain = load_qa_chain(llm, chain_type="stuff")
    db = retrieve_info(body, doc_query)

    with get_openai_callback() as cb:
        response = chain.run(input_documents=db, question=doc_query)
        print('\n> Result Callback:')
        print(cb)

    return response


if __name__ == '__main__':
    qna()
