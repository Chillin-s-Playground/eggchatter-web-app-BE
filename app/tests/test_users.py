import httpx
import pytest
from faker import Faker

from app.schemas.users import CreateProfileDTO

base_url = "http://127.0.0.1:8080/user"
faker = Faker()


def generate_profile_data(is_valid=True):
    """프로필 데이터를 만들어조눈 메소드."""
    if is_valid:
        return CreateProfileDTO(
            user_id=1,
            nickname=faker.name(),
            profile_image=faker.image_url(),
        )
    else:
        return CreateProfileDTO(
            user_id=1,
            nickname=faker.name(),
            profile_image=faker.text(max_nb_chars=300),
        )


# Assignment
@pytest.fixture(scope="function")
def valid_profile_data():
    """유효한 프로필 데이터"""
    return generate_profile_data(is_valid=True)


@pytest.fixture(scope="function")
def invalid_profile_data():
    """유효하지 않은 프로필 데이터"""
    return generate_profile_data(is_valid=False)


# Act
async def run_post_request(path: str, data):
    async with httpx.AsyncClient() as client:
        return await client.post(url=f"{base_url}{path}", json=data.model_dump())


# Assert
@pytest.mark.asyncio
async def test_create_profile_success(valid_profile_data):
    res = await run_post_request(path="/profile", data=valid_profile_data)
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_create_profile_failure(invalid_profile_data):
    res = await run_post_request(path="/profile", data=invalid_profile_data)
    assert res.status_code == 400
