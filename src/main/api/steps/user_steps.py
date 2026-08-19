from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models import credit_repay_request, transfer_request, deposit_request
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.foundation.requesters.crud_requester import CrudRequester

class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def request_credit(self, create_user_request: CreateUserRequest, amount: int):
        account = self.create_account(create_user_request)
        credit_request = CreditRequest(accountId=account.id, amount=amount, termMonths=12)
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created()
        ).post(credit_request)
        return response

    def repay_credit(self, create_user_request: CreateUserRequest):
        account = self.create_account(create_user_request)
        credit_request = CreditRequest(accountId=account.id, amount=5000, termMonths=12)
        credit_response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created()
        ).post(credit_request)

        credit_repay_request = CreditRepayRequest(
            creditId=credit_response.creditId,
            accountId=account.id,
            amount=5000
        )
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(credit_repay_request)
        return response

    def deposit(self, create_user_request: CreateUserRequest):
        account = self.create_account(create_user_request)
        deposit_request = DepositRequest(accountId=account.id, amount=1000)

        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_REQUEST,
            ResponseSpecs.request_ok()
        ).post(deposit_request)
        return response

    def transfer(self, create_user_request: CreateUserRequest, amount: int):
        from_account = self.create_account(create_user_request)

        deposit_request = DepositRequest(accountId=from_account.id, amount=amount)
        ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_REQUEST,
            ResponseSpecs.request_ok()
        ).post(deposit_request)

        to_account = self.create_account(create_user_request)
        transfer_request = TransferRequest(
            fromAccountId=from_account.id,
            toAccountId=to_account.id,
            amount=amount
        )

        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_REQUEST,
            ResponseSpecs.request_ok()
        ).post(transfer_request)
        return response

    def get_info(self, create_user_request: CreateUserRequest, account_id: int):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.GET_INFO,
            ResponseSpecs.request_ok()
        ).get(account_id)
        return response

    def request_credit_invalid(self, create_user_request: CreateUserRequest):
        account = self.create_account(create_user_request)
        credit_request = CreditRequest(accountId=account.id, amount=111111, termMonths=12)
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_bad()
        ).post(credit_request)
        return response

    def repay_credit_invalid(self, create_user_request: CreateUserRequest):
        account = self.create_account(create_user_request)
        credit_request = CreditRequest(accountId=account.id, amount=5000, termMonths=12)
        credit_response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created()
        ).post(credit_request)

        credit_repay_request = CreditRepayRequest(
            creditId=credit_response.creditId,
            accountId=account.id,
            amount=50
        )
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_unprocessable()
        ).post(credit_repay_request)
        return response

    def deposit_invalid(self, create_user_request: CreateUserRequest):
        account = self.create_account(create_user_request)
        deposit_request = DepositRequest(accountId=account.id, amount=333)
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_REQUEST,
            ResponseSpecs.request_bad()
        ).post(deposit_request)
        return response


    def transfer_invalid(self, create_user_request: CreateUserRequest):
        from_account = self.create_account(create_user_request)
        deposit_request = DepositRequest(accountId=from_account.id, amount=1000)
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_REQUEST,
            ResponseSpecs.request_ok()
        ).post(deposit_request)
        to_account = self.create_account(create_user_request)
        transfer_request = TransferRequest(
            fromAccountId=from_account.id,
            toAccountId=to_account.id,
            amount=100
        )
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_REQUEST,
            ResponseSpecs.request_bad()
        ).post(transfer_request)
        return response

    def get_info_invalid(self, create_user_request: CreateUserRequest, account_id: int):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.GET_INFO,
            ResponseSpecs.request_not_found()
        ).get(account_id)
        return response