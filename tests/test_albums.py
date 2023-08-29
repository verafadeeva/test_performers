from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class TestAlbumsAPI:
    URL = '/api/v1/albums/'

    def test_successful_access_for_albums(self, client):
        response = client.get('/api/v1/albums/')
        assert response.status_code == HTTPStatus.OK

    def test_validate_fields(self, client, album):
        response = client.get(f'{self.URL}{album.id}/')
        data = response.data.keys()
        fields = ['id', 'name', 'release_year', 'singer', 'songs']
        assert list(data) == fields

    def test_create_album_with_bad_data(self, client):
        data = {}
        response = client.post(self.URL, data=data)
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_create_album_with_right_data_without_songs(self, client, singer):
        data = {
            "name": "The Album",
            "release_year": 2000,
            "singer": singer,
        }
        response = client.post(self.URL, data=data)
        assert response.status_code == HTTPStatus.CREATED

    def test_create_album_with_right_data_with_songs(self, client, singer):
        data = {
            "name": "The Album",
            "release_year": 2000,
            "singer": singer,
            "songs": [
                {
                    "name": "Song1",
                    "order_num": 1
                },
                {
                    "name": "Song2",
                    "order_num": 2
                },
                {
                    "name": "Song3",
                    "order_num": 3
                },
                    ]
            }
        response = client.post(self.URL, data=data)
        assert response.status_code == HTTPStatus.CREATED

    def test_update_album(self, client, album):
        data_updated = {
            "name": "Nothing",
            "release_year": album.release_year,
            "singer": album.singer,
        }
        response = client.put(f'{self.URL}{album.id}/',
                              data=data_updated,
                              )
        assert response.status_code == HTTPStatus.OK
        assert response.data.get("name") == data_updated.get("name")

    def test_delete_album(self, client, album):
        response = client.delete(f'{self.URL}{album.id}/')
        assert response.status_code == HTTPStatus.NO_CONTENT
