import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from sqlalchemy.orm import Session


@pytest.mark.api
class TestCreditRepay:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)],
        indirect=True
    )
    def test_credit_repay(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.user_steps.repay_credit(create_user_request)
        assert response.creditId is not None, "CreditId exists"

    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)],
        indirect=True
    )
    def test_credit_repay_invalid(self, api_manager: ApiManager, create_user_request: CreateUserRequest):
        assert api_manager.user_steps.repay_credit_invalid(create_user_request).status_code == 422

