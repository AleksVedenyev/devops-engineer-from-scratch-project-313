import os

from sqlmodel import Session

from model import Link

BASE_URL = os.getenv('BASE_URL')


def test_create_link(client):
    response = client.post("/api/links", json={
        "original_url": "yandex.ru",
        "short_name": "ya"
    })
    assert response.status_code == 201
    assert response.json() == {
        "id": response.json()['id'],
        "original_url": "yandex.ru",
        "short_name": "ya",
        "short_url": f"{BASE_URL}/r/ya"
    }


def test_get_links(client, test_db):
    with Session(test_db) as session:
        link1 = Link(
            original_url="yandex.ru",
            short_name="ya"
        )
        link2 = Link(
            original_url="google.com",
            short_name="gogl"
        )
        session.add(link1)
        session.add(link2)
        session.commit()
        response = client.get("/api/links")
        assert response.status_code == 200
        assert response.headers.get("Content-Range") == "links 0-10/2"
        assert response.json() == [
            {
            "id": link1.id,
            "original_url": link1.original_url,
            "short_name": link1.short_name,
            "short_url": f"{BASE_URL}/r/{link1.short_name}"
        },
        {
            "id": link2.id,
            "original_url": link2.original_url,
            "short_name": link2.short_name,
            "short_url": f"{BASE_URL}/r/{link2.short_name}"
        }
        ]


def test_get_links_with_range(client, test_db):
    with Session(test_db) as session:
        link1 = Link(
            original_url="yandex.ru",
            short_name="ya"
        )
        link2 = Link(
            original_url="google.com",
            short_name="gogl"
        )
        link3 = Link(
            original_url="bing.com",
            short_name="bing"
        )
        link4 = Link(
            original_url="example.com",
            short_name="exmpl"
        )
        session.add(link1)
        session.add(link2)
        session.add(link3)
        session.add(link4)
        session.commit()
        response = client.get("/api/links?range=[0,3]")
        assert response.status_code == 200
        assert response.headers.get("Content-Range") == "links 0-3/4"
        assert response.json() == [
            {
            "id": link1.id,
            "original_url": link1.original_url,
            "short_name": link1.short_name,
            "short_url": f"{BASE_URL}/r/{link1.short_name}"
        },
        {
            "id": link2.id,
            "original_url": link2.original_url,
            "short_name": link2.short_name,
            "short_url": f"{BASE_URL}/r/{link2.short_name}"
        },
        {
            "id": link3.id,
            "original_url": link3.original_url,
            "short_name": link3.short_name,
            "short_url": f"{BASE_URL}/r/{link3.short_name}"
        }
        ]


def test_get_links_with_range2(client, test_db):
    with Session(test_db) as session:
        link1 = Link(
            original_url="yandex.ru",
            short_name="ya"
        )
        link2 = Link(
            original_url="google.com",
            short_name="gogl"
        )
        link3 = Link(
            original_url="bing.com",
            short_name="bing"
        )
        link4 = Link(
            original_url="example.com",
            short_name="exmpl"
        )
        session.add(link1)
        session.add(link2)
        session.add(link3)
        session.add(link4)
        session.commit()
        response = client.get("/api/links?range=[2,4]")
        assert response.status_code == 200
        assert response.headers.get("Content-Range") == "links 2-4/4"
        assert response.json() == [
        {
            "id": link3.id,
            "original_url": link3.original_url,
            "short_name": link3.short_name,
            "short_url": f"{BASE_URL}/r/{link3.short_name}"
        },
        {
            "id": link4.id,
            "original_url": link4.original_url,
            "short_name": link4.short_name,
            "short_url": f"{BASE_URL}/r/{link4.short_name}"
        }
        ]


def test_get_link(client, test_db):
    with Session(test_db) as session:
        link1 = Link(
            original_url="yandex.ru",
            short_name="ya"
        )
        session.add(link1)
        session.commit()
        response = client.get(f"/api/links/{link1.id}")
        assert response.status_code == 200
        assert response.json() == {
            "id": link1.id,
            "original_url": link1.original_url,
            "short_name": link1.short_name,
            "short_url": f"{BASE_URL}/r/{link1.short_name}"
        }


def test_put_link(client, test_db):
    with Session(test_db) as session:
        link = Link(
            original_url="yandex.ru",
            short_name="ya"
        )
        session.add(link)
        session.commit()
        response = client.put(f"/api/links/{link.id}", json={
            "original_url": "google.com",
            "short_name": "gogl"
        })
        assert response.status_code == 200
        assert response.json() == {
            "id": link.id,
            "original_url": "google.com",
            "short_name": "gogl",
            "short_url": f"{BASE_URL}/r/gogl"
        }


def test_delete_link(client, test_db):
    with Session(test_db) as session:
        link1 = Link(
            original_url="yandex.ru",
            short_name="ya"
        )
        link2 = Link(
            original_url="google.com",
            short_name="gogl"
        )
        session.add(link1)
        session.add(link2)
        session.commit()
        response = client.delete(f"/api/links/{link2.id}")
        assert response.status_code == 204
        response2 = client.get("/api/links")
        assert response2.json() == [
            {
            "id": link1.id,
            "original_url": link1.original_url,
            "short_name": link1.short_name,
            "short_url": f"{BASE_URL}/r/{link1.short_name}"
        }
        ]