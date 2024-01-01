
import sys
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv

from tmp.prompt import prompt  # NOQA


# 1. Vectorise the csv data
def vectorise(path='./tmp/dat.csv'):
    try:
        loader = CSVLoader(file_path=path)
        documents = loader.load()
    except Exception as e:
        print(e)
        sys.exit(1)

    print(f'> {len(documents)} entries found.')
    return documents


# 2. Function for similarity search
def retrieve_info(src, query):
    result_data = []
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(src, embeddings)
    responses = db.similarity_search(
        query, k=3)  # returns 'list' object

    result_data = [doc.page_content for doc in responses]
    return result_data


# 3-4. Setup LLMChain & prompts; Retrieval augmented generation
def generate_response(query, src_responses):
    # 3. Setup LLMChain & prompts
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")
    prompt_template = PromptTemplate(
        input_variables=['question', 'response'],
        template=prompt())
    chain = LLMChain(llm=llm, prompt=prompt_template)

    # 4. Retrieval augmented generation
    response = chain.run(question=query, response=src_responses)
    return response


def main(query):
    load_dotenv()
    src = vectorise()
    src_responses = retrieve_info(src, query)

    results = generate_response(query, src_responses)

    with open('./results.tmp.md', 'a') as f:
        f.write('### *ENTRY*\n')
        f.write(f'#### Type: {type(results)}\n')
        f.write(f'{results}')
        f.write('\n---\n')

    answers = results.split('a: ')
    # TODO: more logic on splitting answers
    if len(answers) > 1:
        final = answers[1]
    else:
        final = answers[0]
    return final


if __name__ == '__main__':
    main()
