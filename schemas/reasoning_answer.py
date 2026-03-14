from pydantic import BaseModel, Field

class ReasoningAnswer(BaseModel):

    gandire: str = Field(
        description="Pașii logici folosiți pentru a ajunge la răspuns"
    )

    raspuns: str = Field(
        description="Concluzia finală"
    )

    confidence: float = Field(
        ge=0,
        le=1,
        description="Nivelul de încredere în răspuns"
    )