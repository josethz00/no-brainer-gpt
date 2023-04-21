import os
import pinecone

class PineconeVectorDB:
    index: pinecone.Index = None
    manager = pinecone

    def connect(self, index_name: str = 'nobrainer'):
        # Connect Pinecone
        pinecone.init(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_ENV")
        )

        # Create a Pinecone index
        if index_name not in pinecone.list_indexes():
            pinecone.create_index(index_name, dimension=1536) # set 1536 as the dimension of the embeddings, the default of the text-embedding-ada-002 model
        # Connect to the index
        self.index = pinecone.Index(index_name)

vector_db = PineconeVectorDB()
