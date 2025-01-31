import os

from tavily import TavilyClient

from assistent.inference import AIInference
from assistent.state import AssistentState


def run_web_retrieve(state: AssistentState, inference: AIInference):
    tavily_client = TavilyClient(api_key=os.environ['TAVILY_API_KEY'])
    tavily_answer = tavily_client.search(query=state['query'], max_results=3, include_answer="basic")
    state['reasoning'] = tavily_answer['answer']
    state['sources'] = [item['url'] for item in tavily_answer['results']]
    return state