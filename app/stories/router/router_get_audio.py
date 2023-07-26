from typing import Any, List
from fastapi import Depends, Response
from pydantic import Field
from fastapi.responses import JSONResponse
from fastapi import Depends, Response, status
from app.utils import AppModel
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.stories.adapters.audio_service import AudioService
from ..service import Service, get_service
from . import router
import os
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("PLAY_HT_APi_KEY")
user_id = os.getenv("PLAY_HT_USER_ID")
play_ht_service = AudioService(api_key=api_key, api_userid=user_id)


class StoryRequest(AppModel):
    story_id: Any = Field(alias="_id")


@router.post("/create_audio", status_code=201)
def create_audio(
    input: StoryRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):  
    text = svc.repository.get_story(user_id=jwt_data.user_id, story_id=input.story_id)
    audio_url = play_ht_service.text_to_speach(text["content"])
    return Response(audio_url)



