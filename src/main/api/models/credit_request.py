from src.main.api.models.base_model import BaseModel


class CreditRequest(BaseModel):
    accountId: int
    amount: int
    termMonths: int