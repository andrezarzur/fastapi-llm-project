from functools import wraps
from fastapi import HTTPException


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException as http_err:
            raise http_err
        except Exception as err:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(err)}")
    return wrapper
