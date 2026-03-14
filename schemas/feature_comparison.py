from pydantic import BaseModel, Field

class FeatureComparison(BaseModel):
    """O linie din tabelul comparativ."""
    feature_name: str = Field(description="Numele caracteristicii")
    produs_a_value: str = Field(description="Valoare produs A")
    produs_b_value: str = Field(description="Valoare produs B")
    rationale: str = Field(description="Analiză scurtă care explică diferențele dintre produse pentru acest feature și cum influențează preferințele utilizatorului.")
    winner_score: int = Field(ge=1, le=10, description="Diferență 1-10")
    winner: str = Field(pattern="^(A|B|Egal)$")
    relevant_pentru_user: bool