from pydantic import BaseModel, Field
from typing import List
from pydantic import BaseModel



class RecommendationRequest(BaseModel):
    book_name: str = Field(
        ...,
        min_length=1,
        description="Name of the book"
    )

    top_n: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of recommendations"
    )
    

class BookRecommendation(BaseModel):
    title: str
    author: str
    image_url: str


class RecommendationResponse(BaseModel):
    input_book: str = Field(..., description="Input book name")
    total_recommendations: int = Field(..., description="Total number of recommendations")
    recommendations: List[BookRecommendation]
    latency: float = Field(..., description="Latency of the prediction in ms", examples=[0.5, 0.8])
    average_latency: float = Field(..., description="Average latency of the prediction in ms", examples=[0.5, 0.8])