"""
Product Comparison Engine cu Instructor + OpenAI client pentru Ollama.
Garantează output structurat validat Pydantic prin Instructor.
"""

from fastapi import FastAPI
from controllers.comparison_controller import router as comparison_router


app = FastAPI(
    title="Product Comparison cu Instructor",
    description="""
    Comparare produs cu garantie Pydantic via Instructor.

    **Flow:**
    1. Extrage date (scraping sau text)
    2. Instructor + OpenAI client forțează output validat
    3. Returnează JSON garantat valid conform ComparisonResult

    **De ce Instructor?**
    - Garantează schema Pydantic sau reîncearcă automat
    - Nu mai e nevoie de parsing manual JSON
    - Tipuri Python native în tot codul
    """,
    version="3.0.0"
)

app.include_router(comparison_router)
