from assistent.state import AssistentState
from assistent.inference import AIInference
from assistent.structured import GradeAnswer, BoolAnswer
from assistent.prompts import IS_USEFUL

def is_useful(state: AssistentState, inference: AIInference):
    grade = GradeAnswer.model_validate(
        inference.chat_completion(user=IS_USEFUL.format(generation=state['reasoning'], question=state['query']),
                                  structured=GradeAnswer))
    return grade.score == BoolAnswer.YES