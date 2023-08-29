import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from core.models import Album, Performence


@pytest.fixture
def singer(db) -> Performence:
    return Performence.objects.create(name="Singer")


@pytest.fixture
def album(db, singer: Performence) -> Album:
    return Album.objects.create(
        name="Album",
        release_year=2000,
        singer=singer,
        )


@pytest.fixture
def current_year():
    return timezone.now().year


@pytest.fixture
def client():
    client = APIClient()
    return client
