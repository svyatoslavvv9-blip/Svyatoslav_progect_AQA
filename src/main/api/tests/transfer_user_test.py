import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.db.crud.account_crud import AccountCrudDb
@pytest.mark.api
class TestTransferUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)],
        indirect=True
    )
    def test_transfer_user(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.user_steps.transfer(create_user_request, 1000)
        assert response.fromAccountIdBalance == 0
        from_account_db = AccountCrudDb.get_account_by_id(db_session, response.fromAccountId)
        to_account_db = AccountCrudDb.get_account_by_id(db_session, response.toAccountId)
        assert from_account_db.balance == 0, "Баланс отправителя в БД не совпадает"
        assert to_account_db.balance == 1000, "Баланс получателя в БД не совпадает"
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)],
        indirect=True
    )
    def test_transfer_user_invalid(self, api_manager, create_user_request, db_session: Session):
        assert api_manager.user_steps.transfer_invalid(create_user_request).status_code == 400





