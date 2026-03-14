from fastapi import APIRouter, Depends, status
from services.comparison_service import ComparisonService
from dependencies.dependencies import get_comparison_service
from schemas.comparison_result import ComparisonResult
from schemas.comparison_request import ComparisonRequest

router = APIRouter(
    prefix="/comparison"
)

@router.post(
        "/",
        status_code=status.HTTP_200_OK,
        response_model=ComparisonResult
        )
async def compare_products(request: ComparisonRequest, comparison_service: ComparisonService = Depends(get_comparison_service)):
    return await comparison_service.reasoning_pipeline(request)