import chromadb


client = chromadb.PersistentClient(path='../vectorstore')

collection = client.create_collection(name="my_collection")
# collection = client.get_collection(name="my_collection", embedding_function=emb_fn)
