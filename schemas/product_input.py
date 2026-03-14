from pydantic import BaseModel, Field

class ProductInput(BaseModel):
    sursa: str = Field( min_length=3)
    este_url: bool = Field(default=False)

    class Config:
        json_schema_extra = {
            "example": {
                "sursa": "iPhone 15: A16, 6GB RAM, 48MP camera",
                "este_url": False
            }
        }

