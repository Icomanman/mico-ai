
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

from tmp.prompt import prompt as local_prompt  # NOQA
# from tmp.presentation import present as report_prompt  # NOQA
from tmp.code_prompt import code_prompt  # NOQA
from utils.local_embeddings import embed  # NOQA
from utils.document_loader import load_documents  # NOQA

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
def _retrieve_info(src: list, query: str, db_type: str = 'csv') -> List[str]:
    local_path = './dump/faiss' if db_type == 'csv' else './dump/md'
    start = time.time()
    result_data = []
    embeddings = embed()
    # embeddings = OpenAIEmbeddings()

    if os.path.exists(local_path):
        db = FAISS.load_local(local_path, embeddings)
        print('> local db is found at.', local_path)
    else:
        db = FAISS.from_documents(src, embeddings)
        db.save_local(local_path)

    # Returns 'list' of Document object
    responses = db.similarity_search(
        query, k=3)

    # Extracts 'page_content' from the Document object as str and puts the into List Comprehension -> List[str]
    result_data = [doc.page_content for doc in responses]
    print(f'> retrieval: {(time.time() - start)} s')
    return result_data


# 3. Setup prompt:
def _set_prompt(workflow: str = '') -> PromptTemplate:
    if not workflow:
        return ''

    src_prompt = ''
    input_vars = []
    if workflow == 'Knowledge Base':
        input_vars.extend(['question', 'response'])
        src_prompt = local_prompt()
    elif workflow == 'Report':
        input_vars.append('question')
        src_prompt = code_prompt()

    prompt = PromptTemplate(
        input_variables=input_vars, template=src_prompt)
    return prompt


# 4. Setup LLMChain; Retrieval augmented generation
def _generate_response(query: str, src_responses: List[str], prompt_template: PromptTemplate) -> str:
    start = time.time()
    # Setup LLMChain
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")
    chain = LLMChain(llm=llm, prompt=prompt_template)
    print(f'> prompt/chain init: {(time.time() - start)} s')
    start = time.time()
    # Retrieval augmented generation
    response = chain.run(question=query, response=src_responses)
    print(f'> generate: {(time.time() - start)} s')
    return response


def main(query: str, workflow: str) -> str:
    if workflow == 'Knowledge Base':
        src = _vectorise()
        src_responses = _retrieve_info(src, query)
    elif workflow == 'Report':
        src = load_documents(path='./pdf/md/3404.md', src_type='md')
        src_responses = _retrieve_info(src, query, 'md')
    else:
        return

    custom_prompt = _set_prompt(workflow)
    if not custom_prompt:
        raise ValueError('> Unable to generate custom prompt.')

    results = _generate_response(query, src_responses, custom_prompt)
    with open('./results.tmp.md', 'a', encoding='utf-8') as f:
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
