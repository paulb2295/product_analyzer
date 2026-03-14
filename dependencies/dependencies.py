from fastapi import Depends
from services.scraping_service import ScrapingService
from services.comparison_service import ComparisonService

def get_scraping_dependency():
    return ScrapingService()

def get_comparison_service(
        scraping = Depends(get_scraping_dependency)
):
    return ComparisonService(scraping)
