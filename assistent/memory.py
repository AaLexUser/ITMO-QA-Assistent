import chromadb
from chromadb.api.client import Client
import re
from tqdm import tqdm
import json
from pydantic import HttpUrl
from bs4 import BeautifulSoup


from assistent.inference import OpenaiEmbeddings

def extract_main_tag(page_content):
    try:
        soup = BeautifulSoup(page_content, 'html.parser')
        content = soup.find('article')
        return content.get_text(strip=True, separator='\n')
    except Exception as e:
        return None
    
def chunks_split(text: str, max_chunk_length: int = 8191, overlap_ratio: float = 0.1):
    if not (0 <= overlap_ratio < 1):
        raise ValueError("Overlap ratio must be between 0 and 1 (exclusive).")
    
    # Calculate the length of overlap in characters
    overlap_length = int(max_chunk_length * overlap_ratio)
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + max_chunk_length, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start += max_chunk_length - overlap_length
        
    return chunks
    

class Memory:
    def __init__(self, client: Client, collection_name: str, embedding_model: OpenaiEmbeddings):
        self.chroma_client = client
        self.collection_name = collection_name
        # choose cosine similarity for the search
        self.collection = self.chroma_client.get_or_create_collection(self.collection_name, metadata={"hnsw:space": "cosine"}) 

        # Load the embedding model 
        self.embedding_model = embedding_model
        self.id = 0 # the id of the data in the collection
        
    def insert_vectors(self, chunks: list, website: str, url: HttpUrl, title: str):
        results = chunks
        # insert the vectors into the collection
        for result in tqdm(results):
            text_embedding = self.embedding_model.encode(input=result)[0].embedding

            metadata = {
                'website': website,
                'url': url,
                'title': title
            }

            # insert the vectors into the collection
            self.collection.add(
                documents=result,
                ids=f'{self.id}',
                embeddings=text_embedding,
                metadatas=metadata
            )
            self.id += 1
        print('---------------------------------')
        print(f'Finished inserting vectors for <{self.collection_name}>!')
        print('---------------------------------')

    # use the query to search the most similar context
    def search_context(self, query: str, n_results=5) -> dict:
        query_embeddings = self.embedding_model.encode(query)[0].embedding
        results =  self.collection.query(query_embeddings=query_embeddings, n_results=n_results, include=['documents', 'distances', 'metadatas'])
        return results
    
    def search_context_with_metadatas(self, query: str, where: dict, n_results=5) -> dict:
        query_embeddings = self.embedding_model.encode(query)[0].embedding
        results =  self.collection.query(
            query_embeddings=query_embeddings, n_results=n_results, 
            include=['documents', 'distances', 'metadatas'], 
            where=where
        )
        return results
    
    def check_collection_none(self):
        document_count = self.collection.count()
        if document_count == 0:
            print("The collection is empty.")
        else:
            print(f"The collection has {document_count} documents.")

        return document_count