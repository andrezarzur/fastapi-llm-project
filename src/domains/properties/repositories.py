from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.domains.properties.models import Property
import redis
import json


redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)


class PropertyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, property_id: int):
        property = self.db.query(Property).filter(Property.id == property_id).first()
        if not property:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Property with id {property_id} not found"
            )
        return property

    def get_all(self, skip: int = 0, limit: int = 10):
        cached_properties = redis_client.get('cached_properties')

        if cached_properties:
            return json.loads(cached_properties)

        properties = self.db.query(Property).offset(skip).limit(limit).all()

        if not properties:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No properties found"
            )

        redis_client.setex('cached_properties', 60, json.dumps([property.to_dict() for property in properties]))

        return properties

    def create(self, property: Property):
        self.db.add(property)
        self.db.commit()
        self.db.refresh(property)
        return property

    def update(self, property: Property):
        self.db.commit()
        self.db.refresh(property)
        return property

    def delete(self, property_id: int):
        property = self.get_by_id(property_id)
        if not property:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found"
            )
        self.db.delete(property)
        self.db.commit()
        return {"detail": "Property deleted successfully."}
