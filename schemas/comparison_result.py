from pydantic import BaseModel, Field
from schemas.feature_comparison import FeatureComparison
from schemas.reasoning_answer import ReasoningAnswer
from schemas.verdict import Verdict
from typing import List


class ComparisonResult(BaseModel):
    """
    Model final pe care Instructor îl forțează din LLM.
    Dacă LLM returnează JSON invalid, Instructor retrimite automat.
    """
    produs_a_titlu: str = Field(description="Titlu produs A")
    produs_b_titlu: str = Field(description="Titlu produs B")
    features: List[FeatureComparison] = Field(description="Tabel comparativ")
    reasoning_answer: ReasoningAnswer = Field(description="Logica alegerii rezultatului")
    verdict: Verdict
    preferinte_procesate: str = Field(description="Rezumat preferințe user")
    