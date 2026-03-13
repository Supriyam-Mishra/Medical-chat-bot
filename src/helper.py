from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
import torch
from langchain_community.embeddings import HuggingFaceEmbeddings


def load_pdf_files(data):
    loader=DirectoryLoader(data, 
                           glob="**/*.pdf", 
                           show_progress=True, 
                           loader_cls=PyPDFLoader
                           )
    documents=loader.load()
    return documents


def filter_to_minimal_documents(documents: List[Document]) -> List[Document]:
    minimal_documents = []
    for doc in documents:
        minimal_doc = Document(
            page_content=doc.page_content,
            metadata={"source": doc.metadata.get("source", "")}
        )
        minimal_documents.append(minimal_doc)
    return minimal_documents

def text_splitter(documents: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    split_docs = text_splitter.split_documents(documents)
    return split_docs


def download_embeddings():
    model_name='sentence-transformers/all-MiniLM-L6-v2'
    embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"})
    return embeddings

embeddings = download_embeddings()