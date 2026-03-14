from pydantic import BaseModel, Field

class Verdict(BaseModel):
    """Verdict final al comparației."""
    rationale: str = Field(description="Analiza finală care explică logic de ce un produs câștigă în contextul preferințelor utilizatorului.")
    câștigător: str = Field(pattern="^(A|B|Egal)$")
    scor_a: int = Field(ge=0, le=100, description="Scorul pentru primul produs")
    scor_b: int = Field(ge=0, le=100, description="Scorul pentru al doilea produs")
    diferență_semificativă: bool = Field(description="Daca exista o diferenta mare intre produse")
    argument_principal: str = Field(max_length=500)
    compromisuri: str = Field(max_length=500)