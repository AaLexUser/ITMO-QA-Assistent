from enum import Enum
from pydantic import BaseModel, Field

class BoolAnswer(str, Enum):
    YES = "yes"
    NO = "no"

class ChooseAnswer(BaseModel):
    answer: int
    
class IsOptions(BaseModel):
    is_options: BoolAnswer = Field(..., description="Are there answer options in the query, 'yes' or 'no'.")