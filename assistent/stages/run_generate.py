from assistent.state import AssistentState
from assistent.inference import AIInference
from assistent.prompts import GENERATE
from assistent.structured import GenerateWithCitations

def run_generate(state: AssistentState, inference: AIInference):
    docs = state['docs']
    state["generation"] = inference.chat_completion(user=GENERATE.format(documents=docs),
                                                    structured=GenerateWithCitations)
    return state