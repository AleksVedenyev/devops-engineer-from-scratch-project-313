import os
from contextlib import asynccontextmanager
from typing import Annotated

import sentry_sdk
from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import (
    Session,
    SQLModel,
    create_engine,
    select,
)

from model import CreateLink, Link

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/appdb')
BASE_URL = os.getenv('BASE_URL')

engine = create_engine(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    

app = FastAPI(lifespan=lifespan)


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/ping")
def main():
    return "pong"


@app.get("/api/links")
def get_links(session: Annotated[Session, Depends(get_session)]):
    statement = select(Link)
    result = session.exec(statement)
    links = result.all()
    final_links = [
        {
            "id": link.id,
            "original_url": link.original_url,
            "short_name": link.short_name,
            "short_url": f"{BASE_URL}/r/{link.short_name}",
        }
        for link in links
    ]
    return final_links


@app.post("/api/links", status_code=201)
def create_link(
    new_link: CreateLink,
    session: Annotated[Session, Depends(get_session)],
):  
    result = Link(
        original_url=new_link.original_url,
        short_name=new_link.short_name,
        )
    statement = select(Link).where(Link.short_name == result.short_name)
    current_link = session.exec(statement).first()
    if current_link:
        return {
            "id": current_link.id,
            "original_url": current_link.original_url,
            "short_name": current_link.short_name,
            "short_url": f"{BASE_URL}/r/{current_link.short_name}",
            }
    session.add(result)
    session.commit()
    session.refresh(result)
    return {
        "id": result.id,
        "original_url": result.original_url,
        "short_name": result.short_name,
        "short_url": f"{BASE_URL}/r/{result.short_name}",
    }


@app.get("/api/links/{id}")
def get_link(id: int, session: Annotated[Session, Depends(get_session)]):
    statement = select(Link).where(Link.id == id)
    current_link = session.exec(statement).first()
    if current_link:
        return {
            "id": current_link.id,
            "original_url": current_link.original_url,
            "short_name": current_link.short_name,
            "short_url": f"{BASE_URL}/r/{current_link.short_name}",
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Item not found"
    )


@app.put("/api/links/{id}", status_code=200)
def update_link(
    new_link: CreateLink, 
    id: int, 
    session: Annotated[Session, Depends(get_session)]
    ):
    statement = select(Link).where(Link.id == id)
    current_link = session.exec(statement).first()
    if not current_link:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Item not found"
    )
    current_link.original_url = new_link.original_url
    current_link.short_name = new_link.short_name
    session.add(current_link)
    session.commit()
    session.refresh(current_link)
    return {
            "id": id,
            "original_url": new_link.original_url,
            "short_name": new_link.short_name,
            "short_url": f"{BASE_URL}/r/{new_link.short_name}",
        }


@app.delete("/api/links/{id}", status_code=204)
def delete_link(
    id: int, 
    session: Annotated[Session, Depends(get_session)]
    ):
    statement = select(Link).where(Link.id == id)
    current_link = session.exec(statement).first()
    if not current_link:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Item not found"
    )
    session.delete(current_link)
    session.commit()


if __name__ == "__main__":
    main()
