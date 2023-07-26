from typing import Any, List
from fastapi import Depends, Response
from pydantic import Field
from app.utils import AppModel
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.stories.adapters.openai_service1 import OpenAIService
from ..service import Service, get_service
from . import router
import os
from dotenv import load_dotenv


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_service = OpenAIService(api_key=openai_api_key)

class GetStoryResponse(AppModel):
    story: Any

class GetMyStoriesResponse(AppModel):
    stories: List[Any]

@router.get('/{story_id:str}', status_code=200, response_model=GetStoryResponse)
def get_story(
    story_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    story = svc.repository.get_story(user_id=jwt_data.user_id, story_id=story_id)
    if story is None:
        return Response(status_code=404)
    return GetStoryResponse(story=story)

@router.get('/', response_model=GetMyStoriesResponse)
def get_my_stories(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    stories = svc.repository.get_stories(user_id=jwt_data.user_id)
    return GetMyStoriesResponse(stories=stories)