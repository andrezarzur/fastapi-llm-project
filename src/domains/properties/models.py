from sqlalchemy import Column, String, Integer, Float
from src.config.database import Base, engine


class Property(Base):
    __tablename__ = "properties"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    property_type = Column("property_type", String, nullable=False)
    address_full = Column("address_full", String, nullable=False)
    price = Column("price", Float, nullable=False)
    area = Column("area", Integer, nullable=False)
    bedrooms = Column("bedrooms", Integer, nullable=False)
    bathrooms = Column("bathrooms", Integer, nullable=False)
    parking = Column("parking", Integer, nullable=False)
    description = Column("description", String, nullable=False)
    coordinates = Column("coordinates", String, nullable=False)

    def __init__(self, property_type, address_full, price, area, bedrooms, bathrooms, parking, description, coordinates):
        self.property_type = property_type
        self.address_full = address_full
        self.price = price
        self.area = area
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.parking = parking
        self.description = description
        self.coordinates = coordinates

    def to_dict(self):
        return {
            "id": self.id,
            "property_type": self.property_type,
            "address_full": self.address_full,
            "price": self.price,
            "area": self.area,
            "bedrooms": self.bedrooms,
            "bathrooms": self.bathrooms,
            "parking": self.parking,
            "description": self.description,
            "coordinates": self.coordinates
        }


Base.metadata.create_all(bind=engine)
