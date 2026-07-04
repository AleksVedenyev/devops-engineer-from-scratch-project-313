import os

from sqlmodel import Session
from model import CreateLink, Link

BASE_URL = os.getenv('BASE_URL')


def test_create_links(client):
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