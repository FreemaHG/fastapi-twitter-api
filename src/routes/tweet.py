from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models.users import User
from src.services.like import LikeService
from src.services.tweet import TweetsService
from src.utils.user import get_current_user
from src.schemas.tweet import TweetResponseSchema, TweetInSchema, TweetListSchema
from src.schemas.base_response import (
    ResponseSchema,
    UnauthorizedResponseSchema,
    ValidationResponseSchema,
    LockedResponseSchema,
    ErrorResponseSchema
)


router = APIRouter(
    prefix="/api/tweets",  # URL
    tags=["tweets"]  # Объединяем URL в группу
)


@router.get(
    "",
    response_model=TweetListSchema,
    responses={
        401: {"model": UnauthorizedResponseSchema}
    },
    status_code=200
)
async def get_tweets(
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session)
):
    """
    Вывод ленты твитов (выводятся твиты людей, на которых подписан пользователь)
    """
    tweets = await TweetsService.get_tweets(user=current_user, session=session)

    return {"tweets": tweets}


@router.post(
    "",
    response_model=TweetResponseSchema,
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
    response_model=ResponseSchema,
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
