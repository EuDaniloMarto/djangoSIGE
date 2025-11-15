import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def user():
    user = get_user_model().objects.create_user(username="johndoe", password="johndoe@test")
    yield user


@pytest.fixture
def client_logged(client, user):
    client.force_login(user)
    return client
