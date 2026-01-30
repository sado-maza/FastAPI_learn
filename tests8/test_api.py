import pytest
from httpx import AsyncClient,ASGITransport
from main import app



def func(num):
    return 20/num


#/===========================================================\#
#|                          unit test                        |#
#\===========================================================/#

def test_func():
    assert func(2)==10




#/===========================================================\#
#|                      integration test                     |#
#\===========================================================/#

@pytest.mark.asyncio
async def test_get_books():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get('/books')
        assert response.status_code == 200
        data=response.json()
        assert len(data) == 2


@pytest.mark.asyncio
async def test_post_book():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.post('/bookss',json={
            "title": "щ",
            "author": "adfadf",
            "number_of_pages": 23,
            "year_published": "afadfasdfahdfkandf",
        })
        assert response.status_code == 200
        data=response.json()
        assert data["comment"] == "татата"

