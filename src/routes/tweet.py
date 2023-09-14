from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models.users import User
from services.like import LikeService
from services.tweet import TweetsService
from schemas.base_response import ResponseSchema, UnauthorizedResponseSchema, ValidationResponseSchema, \
    LockedResponseSchema, ErrorResponseSchema
from schemas.tweet import TweetResponseSchema, TweetInSchema
from utils.user import get_current_user


router = APIRouter(
    prefix="/tweets",  # URL
    tags=["tweets"]  # Объединяем URL в группу
)


@router.post(
    "",
    # Валидация выходных данных согласно схеме UserOutSchema
    response_model=TweetResponseSchema,
    # Примеры схем ответов для разных кодов ответов сервера
    responses={
        401: {"model": UnauthorizedResponseSchema},
        422: {"model": ValidationResponseSchema},
    },
    status_code=201
)
async def create_tweet(
        tweet: TweetInSchema,
        current_user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session)
):
    """
    Добавление твита
    """
    tweet = await TweetsService.create_tweet(tweet=tweet, current_user=current_user, session=session)

    return {"tweet_id": tweet.id}


@router.delete(
    "/{tweet_id}",
    response_model=ResponseSchema,
    responses={
        401: {"model": UnauthorizedResponseSchema},
        404: {"model": ErrorResponseSchema},
        422: {"model": ValidationResponseSchema},
        423: {"model": LockedResponseSchema},
    },
    status_code=200,
)
async def delete_tweet(
    tweet_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удаление твита
    """
    await TweetsService.delete_tweet(user=current_user, tweet_id=tweet_id, session=session)

    return {"result": True}


@router.post(
    "/{tweet_id}/likes",
    # Валидация выходных данных согласно схеме UserOutSchema
    response_model=ResponseSchema,
    # Примеры схем ответов для разных кодов ответов сервера
    responses={
        401: {"model": UnauthorizedResponseSchema},
        404: {"model": ErrorResponseSchema},
        422: {"model": ValidationResponseSchema},
        423: {"model": LockedResponseSchema},
    },
    status_code=201
)
async def create_like(
        tweet_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session)
):
    """
    Лайк твита
    """
    await LikeService.like(tweet_id=tweet_id, user_id=current_user.id, session=session)

    return {"result": True}


@router.delete(
    "/{tweet_id}/likes",
    response_model=ResponseSchema,
    responses={
        401: {"model": UnauthorizedResponseSchema},
        404: {"model": ErrorResponseSchema},
        422: {"model": ValidationResponseSchema},
        423: {"model": LockedResponseSchema},
    },
    status_code=200,
)
async def delete_like(
    tweet_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удаление лайка
    """
    await LikeService.dislike(tweet_id=tweet_id, user_id=current_user.id, session=session)

    return {"result": True}
