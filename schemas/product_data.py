from pydantic import BaseModel, Field

class ProductData(BaseModel):
    """Date extrase despre produs."""
    titlu: str = Field(description="Numele produsului")
    descriere: str = Field(description="Descriere scurtă")
    specificatii: str = Field(description="Specificații tehnice cheie")
    preț: str = Field(default="")
    extras_din: str = Field(description="'scraping' sau 'text'")

