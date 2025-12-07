from pydantic import BaseModel, Field

# Input Schema
# هذا الكلاس يمثل البيانات التي سيرسلها المستخدم
class HouseFeatures(BaseModel):
    MedInc: float = Field(..., description="Median income in block group", example=3.5)
    HouseAge: float = Field(..., description="Median house age in block group", example=25.0)
    AveRooms: float = Field(..., description="Average number of rooms per household", example=5.0)
    AveBedrms: float = Field(..., description="Average number of bedrooms per household", example=1.0)
    Population: float = Field(..., description="Block group population", example=1000.0)
    AveOccup: float = Field(..., description="Average number of household members", example=3.0)
    Latitude: float = Field(..., description="Block group latitude", example=34.05)
    Longitude: float = Field(..., description="Block group longitude", example=-118.25)

# Output Schema
# هذا الكلاس يمثل رد الـ API
class PricePrediction(BaseModel):
    predicted_price: float = Field(..., description="Predicted price in $100,000s")