import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.models.account_table import Account
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator


@pytest.mark.api
class TestCreditRequest:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)],
        indirect=True
    )
    def test_credit_request(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        credit_response = api_manager.user_steps.request_credit(create_user_request, 5000)
        assert credit_response.balance == 5000, "Money on a account"
        assert AccountCrudDb.get_account_by_id(db_session, credit_response.id).balance == 5000

    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)],
        indirect=True
    )
    def test_credit_request_invalid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        assert api_manager.user_steps.request_credit_invalid(create_user_request).status_code == 400