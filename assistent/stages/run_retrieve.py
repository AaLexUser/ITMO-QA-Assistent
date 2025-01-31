from assistent.state import AssistentState
from assistent.local_retrieve import LocalRetrieve
def run_retrieve(state: AssistentState, retriever: LocalRetrieve) -> AssistentState:
    query = state['query']
    docs_dict = retriever.query('query')
    state['sources'] = [doc_item['metadatas']['url'] for doc_item in docs_dict]
    state['docs'] = '\n'.join(['\n'.join([doc_item['metadatas']['title'],  doc_item['documents']]) for doc_item in docs_dict])
    return state