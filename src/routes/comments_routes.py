from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from src.schemas.comment_schemas import CommentRequest, CommentResponse
from src.dependencies.dependencies import get_session
from src.models.models import Comment, Film, User
from src.auth.dependencies import get_current_user
from src.mappers.comment_mapper import from_request_comment, to_response_comment

comments_router = APIRouter(tags=["comments"])


def build_comment_response(comment: Comment) -> CommentResponse:
    return to_response_comment(comment)


def resolve_film_id_from_parent(session: Session, parent: Comment) -> int:
    current = parent
    while current is not None:
        if current.film_id is not None:
            return current.film_id
        if current.parent_id is None:
            break
        current = session.query(Comment).filter(Comment.id == current.parent_id).first()
    raise HTTPException(status_code=400, detail="Parent comment is not linked to a film")


def sort_replies_recursively(comment: CommentResponse) -> None:
    comment.replies.sort(key=lambda item: item.datetime, reverse=True)
    for reply in comment.replies:
        sort_replies_recursively(reply)


@comments_router.post(
    "/films/{film_id}/comments",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentResponse,
)
async def create_comment_for_film(
    film_id: int,
    payload: CommentRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Cria um novo comentário para um filme. Requer autenticação."""
    film = session.query(Film).filter(Film.id == film_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    payload_data = from_request_comment(payload)
    new_comment = Comment(
        user_id=current_user.id,
        comment_text=payload_data["comment_text"],
        film_id=film_id,
        parent_id=None,
    )
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)

    return build_comment_response(new_comment)


@comments_router.post(
    "/comments/{comment_id}/replies",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentResponse,
)
async def create_reply_for_comment(
    comment_id: int,
    payload: CommentRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Cria uma resposta para um comentário existente. Requer autenticação."""
    parent_comment = session.query(Comment).filter(Comment.id == comment_id).first()
    if not parent_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    film_id = resolve_film_id_from_parent(session, parent_comment)

    payload_data = from_request_comment(payload)
    new_comment = Comment(
        user_id=current_user.id,
        comment_text=payload_data["comment_text"],
        film_id=film_id,
        parent_id=parent_comment.id,
    )
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)

    return build_comment_response(new_comment)


@comments_router.get(
    "/films/{film_id}/comments",
    response_model=list[CommentResponse],
)
async def get_film_comments(
    film_id: int,
    session: Session = Depends(get_session),
):
    """Retorna todos os comentários do filme com replies recursivas."""
    film = session.query(Film).filter(Film.id == film_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    comments = (
        session.query(Comment)
        .options(joinedload(Comment.user))
        .filter(Comment.film_id == film_id)
        .order_by(Comment.datetime.desc())
        .all()
    )

    comment_map: dict[int, CommentResponse] = {}
    roots: list[CommentResponse] = []

    for comment in comments:
        comment_map[comment.id] = build_comment_response(comment)

    for comment in comments:
        node = comment_map[comment.id]
        if comment.parent_id and comment.parent_id in comment_map:
            comment_map[comment.parent_id].replies.append(node)
        else:
            roots.append(node)

    roots.sort(key=lambda item: item.datetime, reverse=True)
    for root in roots:
        sort_replies_recursively(root)

    return roots
