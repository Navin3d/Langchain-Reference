import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.Client()
default_ef = embedding_functions.DefaultEmbeddingFunction()

# switch `create_collection` to `get_or_create_collection` to avoid creating a new collection every time
collection = chroma_client.get_or_create_collection(
    name="my_collection",
    embedding_function=default_ef,
    configuration={
        "embedding_function": default_ef
    }
)

# switch `add` to `upsert` to avoid adding the same documents every time
collection.add(
    documents=["lorem ipsum...", "doc2", "doc3"],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}],
    ids=["id1", "id2", "id3"]
)

results = collection.query(
    query_texts=["This is a query document about florida"], # Chroma will embed this for you
    n_results=1 # how many results to return
)

print(results)
