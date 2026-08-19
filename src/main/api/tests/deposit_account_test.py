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
        [RandomModelGenerator.generate(CreateUserRequest)],
        indirect=True
    )
    def test_deposit_account(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.user_steps.deposit(create_user_request)
        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username
        assert response.balance == 1000, "Баланс != 1000"
        assert AccountCrudDb.get_account_by_id(db_session, response.id).balance == 1000, "Сверяемся с бд"

    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)],
        indirect=True
    )
    def test_deposit_invalid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        assert api_manager.user_steps.deposit_invalid(create_user_request).status_code == 400, 'Пополняем счет пользователя суммой, которая не входит в диапозон допустимых значений'
        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username
