import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.db.crud.account_crud import AccountCrudDb

@pytest.mark.api
class TestTransferUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_transfer_user(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        response_account1 = api_manager.user_steps.create_account(create_user_request)

        assert response_account1.balance == 0

        accountId1 = response_account1.id

        deposit_sum = DepositRequest(accountId=accountId1, amount=1000)

        response = api_manager.user_steps.deposit(create_user_request, deposit_sum)

        assert response.balance == 1000

        response_account2 = api_manager.user_steps.create_account(create_user_request)

        accountId2 = response_account2.id

        transfer_info = TransferRequest(fromAccountId=accountId1, toAccountId=accountId2, amount=1000)

        response = api_manager.user_steps.transfer(create_user_request, transfer_info)
        account1 = api_manager.user_steps.get_info(create_user_request, accountId1)
        account2 = api_manager.user_steps.get_info(create_user_request, accountId2)
        assert AccountCrudDb.get_account_by_id(db_session, accountId1).balance == account1.balance
        assert AccountCrudDb.get_account_by_id(db_session, accountId2).balance == account2.balance
        assert response.fromAccountIdBalance == 0
        assert account2.balance == 1000

    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_transfer_user_invalid(self, api_manager, create_user_request):
        response = api_manager.admin_steps.create_user(create_user_request)
        assert create_user_request.username == response.username
        assert create_user_request.role == response.role
        response_account1 = api_manager.user_steps.create_account(create_user_request)
        assert response_account1.balance == 0
        accountId1 = response_account1.id
        deposit_sum = DepositRequest(accountId=accountId1, amount=1000)
        response = api_manager.user_steps.deposit(create_user_request, deposit_sum)
        assert response.balance == 1000
        response_account2 = api_manager.user_steps.create_account(create_user_request)
        accountId2 = response_account2.id

        transfer_info = TransferRequest(fromAccountId=accountId1, toAccountId=accountId2, amount=1100)

        assert api_manager.user_steps.transfer_invalid(create_user_request, transfer_info).status_code == 422





