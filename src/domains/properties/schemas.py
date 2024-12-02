from pydantic import BaseModel, EmailStr


class PropertyBase(BaseModel):
    property_type: str
    address_full: str
    price: float
    area: int
    bedrooms: int
    bathrooms: int
    parking: int
    description: str or None = None
    coordinate: str or None = None


class PropertyUpdate(BaseModel):
    property_type: str or None = None
    address_full: str or None = None
    price: float or None = None
    area: int or None = None
    bedrooms: int or None = None
    bathrooms: int or None = None
    parking: int or None = None
