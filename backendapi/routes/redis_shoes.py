from fastapi import APIRouter,HTTPException,Body
from ..schemas.schema import Shoe,ColouredItem
from typing import Annotated
from ..utils import redis_utils

router=APIRouter(prefix="/redis_shoes")

@router.post("/latest",response_model= list[Shoe])
def return_latest(n:Annotated[int,Body()]):
    """
    Returns the latest n shoes. If there isn't n shoes available an HTTPException is raised.
    """
    res=redis_utils.read_latest(n)
    if len(res)!=n:
        raise HTTPException(status_code=400,detail="Entries of that much count isn't present")
    return res

@router.post("/latest/color",response_model= list[Shoe])
def return_latest(item:ColouredItem):
    """
    Returns the latest n shoes of the required color. If there isn't n shoes available an HTTPException is raised.
    """
    res=redis_utils.read_latest_by_color(item.color,item.n)
    if len(res)!=item.n:
        raise HTTPException(status_code=400,detail="Entries of that much count isn't present")
    return res