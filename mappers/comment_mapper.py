from schemas.comment_schemas import CommentRequest, CommentResponse
from models.models import Comment


def from_request_comment(payload: CommentRequest) -> dict:
    return {"comment_text": payload.comment_text}


def to_response_comment(comment: Comment) -> CommentResponse:
    return CommentResponse(
        id=comment.id,
        comment_text=comment.comment_text,
        user_id=comment.user_id,
        user_name=comment.user.name if comment.user else "",
        film_id=comment.film_id,
        parent_id=comment.parent_id,
        datetime=comment.datetime,
        replies=[],
    )
