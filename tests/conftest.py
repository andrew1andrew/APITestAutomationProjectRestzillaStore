import pytest
from core.api.auth_api import AuthAPI
from faker import Faker
from typing import Dict

fake = Faker()


@pytest.fixture(scope="session")
def auth_api():
    return AuthAPI()


@pytest.fixture
def random_user() -> Dict[str, str]:
    return {
        "email": fake.email(),
        "password": fake.password()
    }


@pytest.fixture
def registered_user(auth_api, random_user) -> Dict[str, str]:
    auth_api.register(email=random_user["email"], password=random_user["password"])
    return random_user


@pytest.fixture
def logged_in_user(auth_api, registered_user) -> Dict[str, str]:
    response = auth_api.login(email=registered_user["email"], password=registered_user["password"])
    access_token = response.json().get("access_token")
    return {"email": registered_user["email"], "access_token": access_token}


@pytest.fixture(scope="session")
def admin_user(auth_api) -> Dict[str, str]:
    admin_email = "admin@mail.com"
    admin_password = "AdminPassword123!"
    response = auth_api.login(email=admin_email, password=admin_password)
    access_token = response.json().get("access_token")
    return {"email": admin_email, "access_token": access_token}


@pytest.fixture
def auth_token(auth_api, registered_user) -> str:
    response = auth_api.login(registered_user["email"], registered_user["password"])
    return response.json()["access_token"]
