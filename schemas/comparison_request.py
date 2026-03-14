from pydantic import BaseModel, Field
from schemas.product_input import ProductInput
from typing import Optional

class ComparisonRequest(BaseModel):
    produs_a: ProductInput
    produs_b: ProductInput
    preferinte: str = Field(..., min_length=5, max_length=1000)
    buget_maxim: Optional[int] = Field(None, ge=100)
    feedback: Optional[str] = Field(description="Feedback given by another LLM regarding your result, if the result is not ok!")