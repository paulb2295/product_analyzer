from schemas.product_data import ProductData
from schemas.comparison_result import ComparisonResult
from schemas.comparison_request import ComparisonRequest
from schemas.verification_result import VerificationResult
from services.scraping_service import ScrapingService
import instructor
import openai
import os
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()


class ComparisonService:

    def __init__(self, scraping_service: ScrapingService):
        self.client = openai.OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY"), )

        self.instructor_client = instructor.from_openai(self.client, mode=instructor.Mode.JSON)

        self.MODEL_GNERATOR = "llama-3.3-70b-versatile"

        self.MODEL_VALIDATOR = "openai/gpt-oss-120b"

        self.scraping_service = scraping_service

    async def compară_produse_instructor(
            self,
            prod_a: ProductData,
            prod_b: ProductData,
            preferinte: str,
    ) -> ComparisonResult:

        system_prompt = """
        Ești un expert în compararea produselor.

        IMPORTANT:
        Pentru fiecare feature trebuie să explici întâi analiza în câmpul "rationale",
        apoi să alegi câștigătorul.

        Reguli:
        - Analizează diferențele reale
        - Corelează cu preferințele userului
        - Nu alege câștigător fără explicație logică
        """

        user_prompt = f"""Compară aceste produse pentru userul care vrea: "{preferinte}"

                        PRODUS A: {prod_a.titlu}
                        Descriere: {prod_a.descriere[:6000]}
                        Spec: {prod_a.specificatii[:4000]}

                        PRODUS B: {prod_b.titlu}
                        Descriere: {prod_b.descriere[:6000]}
                        Spec: {prod_b.specificatii[:4000]}

                        Generează tabel comparativ cu DOAR feature-urile relevante pentru preferințele userului.
                        Câștigătorul trebuie determinat bazat pe aceste preferințe, nu generic."""

        # INSTRUCTOR AICI: response_model=forțează structura exactă
        try:
            result = self.instructor_client.chat.completions.create(
                model=self.MODEL_GNERATOR,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_model=ComparisonResult,  # MAGIC: garantează validare Pydantic
                max_retries=2,  # Dacă e invalid, retrimite de 2 ori
                temperature=0,
                max_tokens=3000
            )
            return result

        except Exception as e:
            raise HTTPException(503, f"Instructor/LLM error: {str(e)}")

    async def compare(self, request: ComparisonRequest):
        """
        Compară două produse cu Instructor garantat.

        **Exemple:**

        Cu URL:
        ```json
        {
            "produs_a": {"sursa": "https://example.com/laptop-a", "este_url": true},
            "produs_b": {"sursa": "https://example.com/laptop-b", "este_url": true},
            "preferinte": "Programare, 16GB RAM minim, tastatură bună, sub 2kg"
        }
        ```

        Cu text:
        ```json
        {
            "produs_a": {"sursa": "MacBook Air M3 8GB 256GB 1.24kg", "este_url": false},
            "produs_b": {"sursa": "ThinkPad X1 i7 16GB 512GB 1.13kg", "este_url": false},
            "preferinte": "Dezvoltare software și transport zilnic"
        }
        ```
        """
        import time
        start = time.time()

        # Cache key
        # cache_key = f"inv:{hashlib.sha256(request.model_dump_json().encode()).hexdigest()}"
        # cached = cache.get(cache_key)
        # if cached:
        # Reconstruim din cache
        #    return ComparisonResult.model_validate(cached)

        # Extrage date produse
        if request.produs_a.este_url:
            date_a = await self.scraping_service.scrape_product(request.produs_a.sursa)
        else:
            date_a = self.scraping_service.parse_text_input(request.produs_a.sursa)

        if request.produs_b.este_url:
            date_b = await self.scraping_service.scrape_product(request.produs_b.sursa)
        else:
            date_b = self.scraping_service.parse_text_input(request.produs_b.sursa)

        # INSTRUCTOR: Garantat returnează ComparisonResult validat
        result = await self.compară_produse_instructor(date_a, date_b, request.preferinte)

        # Adăugăm metadate
        result_dict = result.model_dump()
        result_dict["_timp_ms"] = int((time.time() - start) * 1000)
        result_dict["_din_cache"] = False

        # Salvăm în cache
        # cache.set(cache_key, result_dict, expire=3600*24)

        return result

    async def verify_reasoning(self, reasoning: ComparisonResult):

        return self.instructor_client.chat.completions.create(
            model=self.MODEL_VALIDATOR,
            response_model=VerificationResult,
            messages=[
                {
                    "role": "system",
                    "content": "Verifică dacă logica este corectă."
                },
                {
                    "role": "user",
                    "content": f"""
    Analizează următoarea logică:

    GANDIRE:
    {reasoning.reasoning_answer.gandire}

    RASPUNS:
    {reasoning.reasoning_answer.raspuns}

    Confidence: {reasoning.reasoning_answer.confidence}

    Este logic valid?
    """
                }
            ]
        )

    async def reasoning_pipeline(self, request: ComparisonRequest):

        for attempt in range(3):

            result = await self.compare(request)

            verification = await self.verify_reasoning(result)

            if verification.verdict == "da":
                return result

            request.feedback = verification.motiv

        return "Couldn't verify reasoning"
