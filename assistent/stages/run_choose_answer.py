from assistent.inference import AIInference
from assistent.state import AssistentState
from assistent.prompts import CHOOSE_ANSWER
from assistent.structured import ChooseAnswer
def run_choose_answer(state: AssistentState, inference: AIInference):
    query = state['query']
    information = state['reasoning']
    is_opt = state['is_opt']
    
    if is_opt:
        choose_answer = ChooseAnswer.model_validate(inference.chat_completion(user=CHOOSE_ANSWER.format(query=query, information=information), structured=ChooseAnswer))
        state['answer'] = choose_answer.answer
    else:
        state['answer'] = None
    return state