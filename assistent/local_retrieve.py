import json
import os

import chromadb
from markdownify import markdownify
from langchain_community.document_loaders import RecursiveUrlLoader
from assistent.inference import OpenaiEmbeddings
from assistent.memory import Memory, chunks_split, extract_main_tag


class LocalRetrieve:
    def __init__(self, embeddings: OpenaiEmbeddings, collection_name: str = 'itmo'):
        self.embeddings = embeddings
        self.client = chromadb.PersistentClient(path='assistent/db')
        self.collection_name = collection_name
        self.db = Memory(self.client, self.collection_name, self.embeddings)
        
    def scrape(self):
        loader = RecursiveUrlLoader(url='https://news.itmo.ru/', max_depth=10)
        docs = loader.load()
        serial_docs = []
        os.makedirs(os.path.dirname('data/raw/itmo_news.json'), exist_ok=True)
        with open('data/raw/itmo_news.json', 'w', encoding='utf-8') as f:
            for doc in docs:
                serial_docs.append(doc.model_dump())
            json.dump(serial_docs, f, ensure_ascii=False, indent=4)
    
    def create_db(self):
        with open('data/raw/itmo_news.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    
        html_pages = list(filter(lambda item: item["metadata"]["content_type"].startswith("text/html"), data))
        docs_main_cont = []   
        for doc in html_pages:
            if content := extract_main_tag(doc['page_content']):
                doc['page_content'] = content
                docs_main_cont.append(doc)

        docs_markdown = []
        for doc in docs_main_cont:
            docm = doc
            docm['page_content'] = markdownify(doc['page_content'])
            docs_markdown.append(docm)
        
        docs_chunks = []
        for doc in docs_markdown:
            docs_chunks.append(
                {
                    'url': doc['metadata']['source'],
                    'title': doc['metadata']['title'],
                    'chunks': chunks_split(text=doc['page_content'], max_chunk_length=2000)
                }
            )
        
        for doc_chunks in docs_chunks:
            self.db.insert_vectors(chunks=doc_chunks['chunks'], website='itmo-news', url=doc_chunks['url'], title=doc_chunks['title'])
                
    def query(self, query: str):
        results = self.db.search_context(query, n_results=3)
        return results