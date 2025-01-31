from functools import partial

from langgraph.graph import END, START, StateGraph

from assistent.inference import AIInference
from assistent.stages import run_web_retrieve, run_is_options, run_choose_answer
from assistent.state import AssistentState


class Assistent:
    def __init__(self, inference: AIInference):
        self.inference = inference
    
    def create_graph(self):
        workflow = StateGraph(AssistentState)
        workflow.add_node("web_retrieve", partial(run_web_retrieve, inference=self.inference))
        workflow.add_node("is_options", partial(run_is_options, inference=self.inference))
        workflow.add_node("choose_answer", partial(run_choose_answer, inference=self.inference))
        
        workflow.add_edge(START, "web_retrieve")
        workflow.add_edge("web_retrieve", "is_options")
        workflow.add_edge("is_options", "choose_answer")
        workflow.add_edge("choose_answer", END)
        
        return workflow.compile()