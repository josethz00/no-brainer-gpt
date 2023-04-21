import pinecone

class PineconeVectorDB:
    index = pinecone.Index('nobrainer')
    manager = pinecone

vector_db = PineconeVectorDB()
