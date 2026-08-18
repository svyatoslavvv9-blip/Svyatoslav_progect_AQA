from typing import List
from src.main.api.models.base_model import BaseModel



class GetResponse(BaseModel):
    id: int
    number: int
    balance: float
    transactions: List