from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api.dependencies import get_db
from src.domains.properties.schemas import PropertyBase
from src.decorators.exception import handle_exceptions
from src.api.dependencies import validate_token_dependency
from src.domains.properties.repositories import PropertyRepository
from src.domains.properties.services import PropertyService
import redis


router = APIRouter(
    prefix="/properties",
    tags=["properties"]
)
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)


@router.get('/')
@handle_exceptions
def get_properties(db: Session = Depends(get_db), _: None = Depends(validate_token_dependency)):
    property_repo = PropertyRepository(db)
    return property_repo.get_all()


@router.get('/{property_id}')
@handle_exceptions
def get_property(property_id: int, db: Session = Depends(get_db), _: None = Depends(validate_token_dependency)):
    print('bn')
    property_repo = PropertyRepository(db)
    return property_repo.get_by_id(property_id)


@router.post('/')
@handle_exceptions
def create_property(property: PropertyBase, db: Session = Depends(get_db), _: None = Depends(validate_token_dependency)):
    property_repo = PropertyRepository(db)
    property_service = PropertyService(property_repo)
    return property_service.create_property(property)


@router.put('/{property_id}')
@handle_exceptions
def update_property(property_id: int, property_update: PropertyBase, db: Session = Depends(get_db), _: None = Depends(validate_token_dependency)):
    property_repo = PropertyRepository(db)
    property_service = PropertyService(property_repo)
    return property_service.update_property(property_id, property_update)


@router.delete('/{property_id}')
@handle_exceptions
def delete_property(property_id: int, db: Session = Depends(get_db), _: None = Depends(validate_token_dependency)):
    property_repo = PropertyRepository(db)
    return property_repo.delete(property_id)
