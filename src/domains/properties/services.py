from .repositories import PropertyRepository
from .schemas import PropertyBase, PropertyUpdate
from fastapi import HTTPException
from .models import Property
from src.services.llm import get_property_description
from src.services.nominatim import NominatimAPI


class PropertyService:
    def __init__(self, property_repo: PropertyRepository):
        self.property_repo = property_repo

    def create_property(self, property: PropertyBase):

        description = get_property_description(property)
        api = NominatimAPI('MyApp/1.0 (https://myapp.dev.net; myapp@gmail.com)')

        coordinates = api.search_location(property.address_full)
        coordinates = parse_coordinates(coordinates)

        property_to_create = Property(
            property_type=property.property_type,
            address_full=property.address_full,
            price=property.price,
            area=property.area,
            bedrooms=property.bedrooms,
            bathrooms=property.bathrooms,
            parking=property.parking,
            description=description,
            coordinates=coordinates
        )

        return self.property_repo.create(property_to_create)

    def update_property(self, property_id: int, property_data: PropertyUpdate):
        property = self.property_repo.get_by_id(property_id)

        if not property:
            raise HTTPException(status_code=404, detail="Property not found")

        if property_data.address_full != property.address_full:
            description = get_property_description(property)
            property.description = description

            api = NominatimAPI('MyApp/1.0 (https://myapp.dev.net; myapp@gmail.com)')
            coordinates = api.search_location(property.address_full)

            coordinates = parse_coordinates(coordinates)

            property.coordinates = coordinates

        for field, value in property_data:
            if value is not None:
                setattr(property, field, value)

        return self.property_repo.update(property)


def parse_coordinates(coordinates):
    if not coordinates:
        coordinates = '0 0'
    else:
        coordinates = str(coordinates[0]['lat']) + ' ' + str(coordinates[0]['lon'])
    return coordinates
