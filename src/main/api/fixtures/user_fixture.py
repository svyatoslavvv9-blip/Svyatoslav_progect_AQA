import pytest

@pytest.fixture
def create_user_request(request, api_manager):
    user_request = request.param
    api_manager.admin_steps.create_user(user_request)
    return user_request