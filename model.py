from datetime import datetime

from sqlalchemy import func
from sqlmodel import Field, SQLModel


class Link(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    original_url: str
    short_name: str = Field(unique=True)
    created_at: datetime | None = Field(
        default=None,
        sa_column_kwargs={"server_default": func.now(), "nullable": False}
    )


class CreateLink(SQLModel):
    original_url: str
    short_name: str = Field(unique=True)
