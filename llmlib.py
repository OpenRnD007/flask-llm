import getpass
import os
import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

def load_documents(file_type, file_path):
    """
    Load documents from a given file path based on the file type.

    :param file_type: The type of the file ('JSON' or 'PDF').
    :param file_path: The path to the file.
    :return: Loaded documents.
    """
    if file_type == 'JSON':
        loader = TextLoader(file_path)
    elif file_type == 'PDF':
        loader = PyPDFLoader(file_path, extract_images=True)
    else:
        raise ValueError("Unsupported file type provided.")
    return loader.load()

def split_documents(docs):
    """
    Split documents into chunks for processing.

    :param docs: Documents to be split.
    :return: List of document chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(docs)

def index_documents(splits):
    """
    Index document chunks and create a vector store.

    :param splits: Chunks of documents to be indexed.
    :return: Vector store of indexed document chunks.
    """
    return Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

def retrieve_and_generate(vector_store, question):
    """
    Retrieve relevant document chunks and generate a response based on a question.

    :param vector_store: Vector store containing indexed document chunks.
    :param question: Question to retrieve and generate a response for.
    :return: Generated response.
    """
    retriever = vector_store.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain.invoke(question)

def llm_app(file_type, file_path, questions):
    """
    Main application function that processes a file and generates a response to the questions.

    :param file_type: The type of the file ('JSON' or 'PDF').
    :param file_path: The path to the file.
    :param question: Questions to generate a response for.
    :return: Generated response.
    """
    docs = load_documents(file_type, file_path)
    splits = split_documents(docs)
    vector_store = index_documents(splits)
    final_result = []
    for question in questions:
        final_result.append({question: retrieve_and_generate(vector_store, question)})
    return final_result

# Example usage
if __name__ == "__main__":
    file_type = 'JSON'
    file_path = './sample-json-kb.txt'
    question = ["display the results of the Company's latest pen test"]
    print(llm_app(file_type, file_path, question))