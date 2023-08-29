from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class TestSingersAPI:
    URL = '/api/v1/singers/'

    def test_successful_access_for_singers(self, client):
        response = client.get(self.URL)
        assert response.status_code == HTTPStatus.OK

    def test_validate_fields(self, client, singer):
        response = client.get(f'{self.URL}{singer.id}/')
        data = response.data.keys()
        assert list(data) == ['id', 'name', 'albums']

    def test_create_singer_with_bad_data(self, client):
        data = {}
        response = client.post(self.URL, data=data)
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_create_singer_with_right_data(self, client):
        data = {
            "name": "Scorpions",
        }
        response = client.post(self.URL, data=data)
        assert response.status_code == HTTPStatus.CREATED

    def test_update_singer(self, client, singer):
        data_updated = {
            "name": "The Beatles",
        }
        response = client.put(f'{self.URL}{singer.id}/',
                              data=data_updated,
                              )
        assert response.status_code == HTTPStatus.OK
        assert response.data.get("name") == data_updated.get("name")

    def test_delete_singer(self, client, singer):
        response = client.delete(f'{self.URL}{singer.id}/')
        assert response.status_code == HTTPStatus.NO_CONTENT
