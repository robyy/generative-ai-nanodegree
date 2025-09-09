import chromadb
from sentence_transformers import SentenceTransformer
import json

class HomeMatchDB:
    def __init__(self, path="./chroma_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name="real_estate_listings")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def _generate_embedding(self, text):
        return self.model.encode(text).tolist()

    def add_listings(self, listings_file="listings.json"):
        with open(listings_file, "r") as f:
            listings = json.load(f)

        documents = []
        metadatas = []
        ids = []

        for i, listing in enumerate(listings):
            # Create a unique ID for each listing
            listing_id = f"listing_{i}"
            ids.append(listing_id)

            # Create a document string for embedding
            document_text = f"Neighborhood: {listing['neighborhood']}\n"
            document_text += f"Price: ${listing['price']}\n"
            document_text += f"Bedrooms: {listing['bedrooms']}\n"
            document_text += f"Bathrooms: {listing['bathrooms']}\n"
            document_text += f"House Size: {listing['house_size']} sqft\n"
            document_text += f"Description: {listing['description']}\n"
            document_text += f"Neighborhood Description: {listing['neighborhood_description']}"
            documents.append(document_text)

            # Store original listing data as metadata
            metadatas.append(listing)

        # Add documents to the collection in batches
        # ChromaDB can handle adding multiple documents at once
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added {len(listings)} listings to ChromaDB.")

    def search_listings(self, query, n_results=5):
        query_embedding = self._generate_embedding(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=['documents', 'metadatas']
        )
        return results

if __name__ == "__main__":
    db = HomeMatchDB()
    db.add_listings()

    # Example search
    query = "I am looking for a family home with a big backyard in a quiet neighborhood."
    search_results = db.search_listings(query)
    print("\nSearch Results:")
    for i, metadata in enumerate(search_results['metadatas'][0]):
        print(f"Result {i+1}:")
        print(f"  Neighborhood: {metadata['neighborhood']}")
        print(f"  Price: ${metadata['price']}")
        print(f"  Description: {metadata['description'][:100]}...") # Print first 100 chars
        print("---")
