from pydantic import BaseModel, Field


class VerificationResult(BaseModel):

    verdict: str = Field(
        pattern="^(da|nu|nesigur)$",
        description="Dacă logica este corectă"
    )

    motiv: str = Field(
        description="Motivul deciziei"
    )