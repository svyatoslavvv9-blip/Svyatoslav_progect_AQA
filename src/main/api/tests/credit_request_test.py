import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator


@pytest.mark.api
class TestCreditRequest:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_credit_request(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0

        accountId = response.id
        credit_request = CreditRequest(accountId=accountId, amount=5000, termMonths=12)

        credit_response = api_manager.user_steps.request_credit(create_user_request, credit_request)
        assert credit_response.balance == 5000
        assert AccountCrudDb.get_account_by_id(db_session, accountId).balance == 5000

    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_credit_request_invalid(self, api_manager, create_user_request):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0

        accountId = response.id
        credit_request = CreditRequest(accountId=accountId, amount=5000, termMonths=12)

        credit_response = api_manager.user_steps.request_credit(create_user_request, credit_request)
        assert credit_response.balance == 5000
        credit_response = api_manager.user_steps.request_credit_invalid(create_user_request, credit_request)
        assert credit_response.status_code == 404