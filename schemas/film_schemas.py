from pydantic import BaseModel, ConfigDict


class FilmRequest(BaseModel):
    name: str
    genre: str
    description: str
    release_year: int

    model_config = ConfigDict(from_attributes=True)


class FilmResponse(BaseModel):
    name: str
    genre: str
    description: str
    release_year: int

    model_config = ConfigDict(from_attributes=True)
