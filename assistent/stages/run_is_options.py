from assistent.inference import AIInference
from assistent.state import AssistentState
from assistent.prompts import IS_OPTIONS
from assistent.structured import IsOptions, BoolAnswer
def run_is_options(state: AssistentState, inference: AIInference):
    query = state['query']
    information = state['reasoning']
    result = IsOptions.model_validate(inference.chat_completion(user=IS_OPTIONS.format(query=query, information=information), structured=IsOptions))
    if (result.is_options == BoolAnswer.YES):
        state['is_opt'] = True
    elif (result.is_options == BoolAnswer.NO):
        state['is_opt'] = False
    else:
        raise ValueError("Invalid answer from the model")
    return state