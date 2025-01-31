from typing import TypedDict, List, Optional
from pydantic import HttpUrl

class AssistentState(TypedDict):
    query: str
    answer: Optional[int]
    reasoning: str
    sources: List[HttpUrl]
    is_opt: bool
    docs: List[str]
    generation: str