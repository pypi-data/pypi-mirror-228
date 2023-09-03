from pydantic import BaseModel
from typing import Optional, Union, Dict

class ObjectResult(BaseModel):
    object: Dict
    
class DeleteResult(BaseModel):
    id: Union[str, int]


class ResultToken(BaseModel):
    token: Optional[str] = None
    refreshToken: Optional[str] = None

class SearchResult(BaseModel):
        items: Optional[list[ObjectResult]] = []
        total: int
        totalPages: int
        page: int
        size: int
        nextPage: Optional[int] = None
        previousPage: Optional[int] = None

class ResponseDTO(BaseModel):
    resultToken: Optional[ResultToken] = None
    resultObject: Union[SearchResult,DeleteResult,ObjectResult,SearchResult, None] = None
    message:  Optional[str] = None
    status: Optional[str] = None
    isError: Optional[bool] = False