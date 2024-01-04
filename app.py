
import sys
from typing import List
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv

from tmp.prompt import prompt  # NOQA


# 1. Vectorise the csv data (this only converst the csv into a list of Document object)
def _vectorise(path='./tmp/dat.csv') -> List[Document]:
    try:
        loader = CSVLoader(file_path=path)
        documents = loader.load()
    except Exception as e:
        print(e)
        sys.exit(1)

    print(f'> {len(documents)} entries found.')
    return documents


# 2. Function for similarity search
def retrieve_info(src: list, query: str) -> List[str]:
    result_data = []
    # These 2 lines are actually responsible for vectorisation
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(src, embeddings)

    # Returns 'list' of Document object
    responses = db.similarity_search(
        query, k=3)

    # Extracts 'page_content' from the Document object as str and puts the into List Comprehension -> List[str]
    result_data = [doc.page_content for doc in responses]
    return result_data


# 3-4. Setup LLMChain & prompts; Retrieval augmented generation
def _generate_response(query: str, src_responses: List[str]) -> str:
    # 3. Setup LLMChain & prompts
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")
    prompt_template = PromptTemplate(
        input_variables=['question', 'response'],
        template=prompt())
    chain = LLMChain(llm=llm, prompt=prompt_template)

    # 4. Retrieval augmented generation
    response = chain.run(question=query, response=src_responses)
    return response


def main(query: str) -> str:
    load_dotenv()
    src = _vectorise()
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
