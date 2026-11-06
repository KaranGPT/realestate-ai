from decimal import Decimal

from httpx import AsyncClient


def make_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "title": "3BHK flat near market",
        "city": "Bhairahawa",
        "price": 5500000,
    }
    payload.update(overrides)
    return payload


async def test_create_property(client: AsyncClient) -> None:
    response = await client.post("/properties", json=make_payload())

    assert response.status_code == 201
    body = response.json()
    assert isinstance(body["id"], int)
    assert body["city"] == "Bhairahawa"
    assert Decimal(body["price"]) == Decimal("5500000")


async def test_create_rejects_negative_price(client: AsyncClient) -> None:
    response = await client.post("/properties", json=make_payload(price=-5))

    assert response.status_code == 422


async def test_create_rejects_short_city(client: AsyncClient) -> None:
    response = await client.post("/properties", json=make_payload(city="B"))

    assert response.status_code == 422


async def test_list_filters_by_city_case_insensitive(client: AsyncClient) -> None:
    await client.post("/properties", json=make_payload(city="Bhairahawa"))
    await client.post("/properties", json=make_payload(city="Bhairahawa", title="Plot on highway"))
    await client.post("/properties", json=make_payload(city="Butwal"))

    response = await client.get("/properties", params={"city": "bhairahawa"})

    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_list_respects_limit(client: AsyncClient) -> None:
    for i in range(3):
        await client.post("/properties", json=make_payload(title=f"Property number {i}"))

    response = await client.get("/properties", params={"limit": 2})

    assert len(response.json()) == 2


async def test_get_property_by_id(client: AsyncClient) -> None:
    created = (await client.post("/properties", json=make_payload())).json()

    response = await client.get(f"/properties/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


async def test_get_missing_property_returns_404(client: AsyncClient) -> None:
    response = await client.get("/properties/9999")

    assert response.status_code == 404


async def test_patch_updates_only_given_fields(client: AsyncClient) -> None:
    created = (await client.post("/properties", json=make_payload())).json()

    response = await client.patch(f"/properties/{created['id']}", json={"price": 6000000})

    assert response.status_code == 200
    body = response.json()
    assert Decimal(body["price"]) == Decimal("6000000")
    assert body["title"] == created["title"]


async def test_patch_rejects_null_field(client: AsyncClient) -> None:
    created = (await client.post("/properties", json=make_payload())).json()

    response = await client.patch(f"/properties/{created['id']}", json={"title": None})

    assert response.status_code == 422


async def test_delete_property(client: AsyncClient) -> None:
    created = (await client.post("/properties", json=make_payload())).json()

    response = await client.delete(f"/properties/{created['id']}")
    assert response.status_code == 204

    follow_up = await client.get(f"/properties/{created['id']}")
    assert follow_up.status_code == 404
