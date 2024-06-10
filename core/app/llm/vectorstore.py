import chromadb
from langchain_chroma import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings


persistent_client = chromadb.PersistentClient(path='../vectorstore')
embedding_function = GPT4AllEmbeddings(
    model_name='all-MiniLM-L6-v2.gguf2.f16.gguf')


def add_docs_to_vectorstore(docs, collection_name):
    langchain_chroma = Chroma(
        client=persistent_client,
        collection_name=collection_name,
        embedding_function=embedding_function,
    )
    langchain_chroma.add_documents(docs)
