import pinecone

class PineconeVectorDB:
    index: pinecone.Index = None
    manager = pinecone

    def connect(self, index_name: str = 'nobrainer'):
        self.index = self.manager.Index(index_name)

vector_db = PineconeVectorDB()
