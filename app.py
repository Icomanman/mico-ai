
import os
import sys
import time
from typing import List
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

# from tmp.prompt import prompt  # NOQA
from utils.local_embeddings import embed  # NOQA
from utils.document_loader import load_documents  # NOQA
# from tmp.presentation import present  # NOQA

# 1. Vectorise the csv data (this only converst the csv into a list of Document object)


def _vectorise(path='./tmp/dat.csv') -> List[Document]:
    start = time.time()
    try:
        loader = CSVLoader(file_path=path)
        documents = loader.load()
    except Exception as e:
        print(e)
        sys.exit(1)

    print(f'> {len(documents)} entries found.')
    print(f'> csv: {(time.time() - start)} s')
    return documents


# 2. Function for similarity search
def retrieve_info(src: list, query: str) -> List[str]:
    start = time.time()
    result_data = []
    # These 2 lines are actually responsible for vectorisation
    # embeddings = OpenAIEmbeddings()
    embeddings = embed()
    db = FAISS.from_documents(src, embeddings)

    # Returns 'list' of Document object
    responses = db.similarity_search(
        query, k=2)

    # Extracts 'page_content' from the Document object as str and puts the into List Comprehension -> List[str]
    result_data = [doc.page_content for doc in responses]
    print(f'> retrieval: {(time.time() - start)} s')
    return result_data


# 3-4. Setup LLMChain & prompts; Retrieval augmented generation
def _generate_response(query: str, src_responses: List[str]) -> str:
    start = time.time()
    # 3. Setup LLMChain & prompts
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")

    PROMPT = os.environ.get('PROMPT')

    prompt_template = PromptTemplate(
        input_variables=['question'], template=PROMPT)
    chain = LLMChain(llm=llm, prompt=prompt_template)

    print(f'> prompt/chain init: {(time.time() - start)} s')
    start = time.time()

    # 4. Retrieval augmented generation
    response = chain.run(question=query, response=src_responses)
    print(f'> generate: {(time.time() - start)} s')
    return response


def main(query: str) -> str:
    load_dotenv()

    # src = _vectorise()
    src = load_documents(path='./pdf/md', src_type='md')
    # src = load_documents(path='./pdf/src', src_type='pdf')

    src_responses = retrieve_info(src, query)
    results = _generate_response(query, src_responses)

    with open('./results.tmp.md', 'a') as f:
        f.write('### *ENTRY*\n')
        f.write(f'#### Type: {type(results)}\n')
        f.write(f'{results}')
        f.write('\n---\n')

    try:
        answers = results.split('a: ')
    except:
        answers = results
    # TODO: more logic on splitting answers
    if len(answers) > 1:
        final = answers[1]
    else:
        final = answers[0]
    return final


if __name__ == '__main__':
    main()
