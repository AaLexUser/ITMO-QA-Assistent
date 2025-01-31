from enum import Enum
from pydantic import BaseModel, Field
from typing import List

class BoolAnswer(str, Enum):
    YES = "yes"
    NO = "no"

class ChooseAnswer(BaseModel):
    answer: int
    
class IsOptions(BaseModel):
    is_options: BoolAnswer = Field(..., description="Are there answer options in the query, 'yes' or 'no'.")
    
class Citation(BaseModel):
    page_title: str = Field(...,
                            description="The title of the page where the citation was found."
                            )
    url: str = Field(...,
                     description="The URL source of the page where the citation was found.")
    number: int = Field(...,
                        description="The number of the citation."
                        )
    relevant_passages: List[str] = Field(...,
                                         description="A list of every relevant passage on a single documentation page."
                                         )


class GenerateWithCitations(BaseModel):
    """Generate a response with citations to relevant passages in the documentation."""

    citations: List[Citation] = Field(...,
                                      description="A list of citations to relevant passages in the documentation."
                                      )

    answer: str = Field(...,
                        description="A plain text answer."
                        )
    
class GradeAnswer(BaseModel):
    """Binary score for hallucination check on generated answer."""

    score: BoolAnswer = Field(...,
                              description="Answer is useful to resolve a question, 'yes' or 'no'."
                              )