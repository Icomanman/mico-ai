
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
    similar_responses = db.similarity_search(
        query, k=3)  # returns 'list' object

    # f = open('./doc.tmp.txt', 'r')
    # similar_responses = f.read()
    # print(similar_responses)

    page_contents_arr = [doc.page_content for doc in similar_responses]

    # for content in page_contents_arr:
    #     print(type(content))
    #     print(content)
    #     answers = [entry.a for entry in content]
    #     complement = [entry.p for entry in content]

    #     result_data.append((query, answers, complement))

    # f.close()
    return page_contents_arr
    # return result_data

# 4. Retrieval augmented generation
# def generate_response(message):
#     best_practice = retrieve_info(message)
#     response = chain.run(message=message, best_practice=best_practice)
#     return response


def main():
    # load_dotenv()
    # src = vectorise()
    msg = 'How can I adapt to the changing environment of the civil engineering industry?'
    # results = retrieve_info(src, msg)

    # 3. Setup LLMChain & prompts
    # llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")
    template = prompt()

    tmp = """
    Say you are a Civil and Structural engineer with 4 decades of experience while having an up-to-date knowledge 
    of the developments in the industry, including but not limited to technology. 
    You are to answer certain questions that will help someone 
    to navigate their career and the industry in general.

    In line with this, I will share some sample questions with their corresponding answers,
    tips and advice with you and you will give the best answer to such questions 
    while you follow ALL of the rules below:

    1/ Response should be very similar or even identical to the tips and advice, 
    in terms of length, tone of voice, logical arguments and other details.

    2/ If the tips and advice are irrelevant to the question, 
    then try to mimic the style of the tips and advice for the corresponding question.

    Below is a sample question:
    {question}

    Here is a list of best practies of how we normally respond to prospect in similar scenarios:
    {response}

    Please write the best response for the interest of the 
    """

    # prompt_template = PromptTemplate(
    #     input_variables=["question", "response"],
    #     template=tmp
    # )

    # chain = LLMChain(llm=llm, prompt=prompt_template)

    # 4. Retrieval augmented generation
    # response = chain.run(question=msg, response=results)

    # print(response)
    # with open('./response.tmp.txt', 'w+') as f:
    #     f.write(f'{response}')

    return


if __name__ == '__main__':
    main()
