import chromadb

client = chromadb.PersistentClient(path="./vectordb")

collection = client.get_or_create_collection("AMCOST_genai")

collection.add(
    documents = ["ChromaDB is a vector database.", "Persistent storage saves data to disk."],
    metadatas = [{"sources" :"docs"},{"sources":"amcost.pdf"}],
    ids = ["docs1", "docs2"]
)

result = collection.query(
    query_texts = ["what is chromadb ?"],
    n_results = 1
)

print(result)