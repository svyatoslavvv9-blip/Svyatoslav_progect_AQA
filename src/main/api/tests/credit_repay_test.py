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
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_credit_repay(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0

        accountId = response.id
        credit_request = CreditRequest(accountId=accountId, amount=5000, termMonths=12)

        credit_response = api_manager.user_steps.request_credit(create_user_request, credit_request)

        creditId = credit_response.creditId
        assert credit_response.balance == 5000



        credit_repay_request = CreditRepayRequest(creditId=creditId, accountId=accountId, amount=5000)

        credit_repay_response = api_manager.user_steps.repay_credit(create_user_request, credit_repay_request)

        account_after_credit_repay = api_manager.user_steps.get_info(create_user_request, accountId)
        assert credit_repay_response.creditId == creditId
        assert AccountCrudDb.get_account_by_id(db_session, accountId).balance == account_after_credit_repay.balance

    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_credit_repay_invalid(self, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0

        creditId = 1111

        accountId = response.id
        credit_request = CreditRequest(accountId=accountId, amount=5000, termMonths=12)

        api_manager.user_steps.request_credit(create_user_request, credit_request)

        credit_repay_request = CreditRepayRequest(creditId=creditId, accountId=accountId, amount=5000)
        response = api_manager.user_steps.repay_credit_invalid(create_user_request, credit_repay_request)
        assert response.status_code == 404
