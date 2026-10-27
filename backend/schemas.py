from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    isbn: str = Field(min_length=10, max_length=17)
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: str | None = None
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    isbn: str
    title: str
    author: str
    description: str | None
    price: float
    stock: int