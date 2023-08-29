import pytest
from django.core.exceptions import ValidationError


def test_validate_right_release_year(album, current_year):
    assert album.release_year < current_year


def test_validate_wrong_release_year(album, current_year):
    album.release_year = current_year + 1
    with pytest.raises(ValidationError):
        album.full_clean()
