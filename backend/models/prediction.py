from pydantic import BaseModel, Field

class PredictionModel(BaseModel):
    accommodates: int = Field(...)
    bedrooms: int = Field(...)
    beds: int = Field(...)
    neighbourhood: str = Field(...)
    bathroom_type: str = Field(...)
    property_type: str = Field(...)
    room_type: str = Field(...)
    amenities: list = Field(...)