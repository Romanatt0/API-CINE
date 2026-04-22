from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CommentRequest(BaseModel):
    comment_text: str

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(CommentRequest):
    pass


class CommentResponse(BaseModel):
    id: int
    comment_text: str
    user_id: int
    user_name: str
    film_id: int | None
    parent_id: int | None
    datetime: datetime
    replies: list["CommentResponse"] = []

    model_config = ConfigDict(from_attributes=True)


CommentResponse.model_rebuild()
