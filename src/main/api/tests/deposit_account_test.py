import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User

@pytest.mark.api
class TestDepositAccount:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_deposit_account(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username

        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0

        accountId = response.id

        deposit_sum = DepositRequest(accountId=accountId, amount=1000)

        response = api_manager.user_steps.deposit(create_user_request, deposit_sum)

        assert response.balance == 1000
        assert AccountCrudDb.get_account_by_id(db_session, response.id).balance == 1000


    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_account_invalid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0

        accountId = response.id

        deposit_sum = DepositRequest(accountId=accountId, amount=10)

        assert api_manager.user_steps.deposit_invalid(create_user_request, deposit_sum).status_code == 400