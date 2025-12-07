from pydantic import BaseModel
from datetime import datetime
from typing import Any

class PredictionResponse(BaseModel):
    id: int
    input_data: Any  # JSON data
    predicted_price: float
    created_at: datetime

    class Config:
        from_attributes = True