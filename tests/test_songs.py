from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class TestSongsAPI:

    def test_successful_access_for_songs(self, client):
        response = client.get('/api/v1/songs/')
        assert response.status_code == HTTPStatus.OK
