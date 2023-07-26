from typing import Any, List
from fastapi import Depends, Response
from pydantic import Field
from app.utils import AppModel
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.stories.adapters.openai_service import OpenAIService
from ..service import Service, get_service
from . import router
import os
from dotenv import load_dotenv


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_service = OpenAIService(api_key=openai_api_key)


class CreateStoryQ1Request(AppModel):
    answer: str = Field(default="Who are the main characters?")


class CreateStoryQ2Request(AppModel):
    story_id: Any = Field(alias="_id")
    question: str = Field(default="question")
    answer: str = Field(default="answer")


class CreateStoryResponse(AppModel):
    inserted_id: Any = Field(alias="_id")
    generated_story: str
    next_question: str


@router.post("/question1", status_code=201, response_model=CreateStoryResponse)
def create_part_1(
    input: CreateStoryQ1Request,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):  
    user = openai_service.create_user(user_id=jwt_data.user_id, characters=input.answer)
    prompt = f"""Who are the main characters?\n{input.answer}. THIS PART IS FOR INTRODUCTION. Introduce and describe the main characters of the story DO NOT MAKE THE END OF STORY!!!!!, THERE WILL BE MORE CONTINUATION OF THE STORY'"""
    generated_story = openai_service.generate_story(user=user, answer=prompt)
    inserted_id = svc.repository.create_story(
        user_id=jwt_data.user_id, content=generated_story, title=""
    )
    question = openai_service.generate_question(user=user, story=generated_story)
    return CreateStoryResponse(inserted_id=inserted_id, 
                               generated_story=str(generated_story), 
                               next_question=question)


@router.post("/question2")
def create_part_2(
    input: CreateStoryQ2Request,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):  
    user = openai_service.get_user(user_id=jwt_data.user_id)
    previous_story = svc.repository.get_previous_story(user_id=jwt_data.user_id, 
                                                       story_id=input.story_id)
    prompt = f'{input.question} : {input.answer}.\n THIS PART IS FOR RISING ACTION. Develop the story. DO NOT MAKE THE END OF STORY!!!!!, THERE WILL BE MORE CONTINUATION OF THE STORY'
    generated_story = openai_service.generate_story(user=user, answer=prompt)
    
    svc.repository.add_part_of_story(
        user_id=jwt_data.user_id, story_id=input.story_id, content=generated_story
    ) 
    question = openai_service.generate_question(user=user, story=previous_story)

    return CreateStoryResponse(inserted_id=input.story_id, 
                               generated_story=str(generated_story), 
                               next_question=question)

@router.post("/question3")
def create_part_3(
    input: CreateStoryQ2Request,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):  
    
    user = openai_service.get_user(user_id=jwt_data.user_id)

    previous_story = svc.repository.get_previous_story(user_id=jwt_data.user_id, 
                                                       story_id=input.story_id)

    prompt = f'{input.question} : {input.answer}.\n  THIS PART IS FOR CLIMAX. Describe the climax of the story. DO NOT MAKE THE END OF STORY!!!!!, THERE WILL BE MORE CONTINUATION OF THE STORY'
    generated_story = openai_service.generate_story(user=user, answer=prompt)
    
    svc.repository.add_part_of_story(
        user_id=jwt_data.user_id, story_id=input.story_id, content=generated_story
    ) 

    question = openai_service.generate_question(user=user, story=previous_story)

    return CreateStoryResponse(inserted_id=input.story_id, 
                               generated_story=str(generated_story), 
                               next_question=question)


@router.post("/question4")
def create_part_4(
    input: CreateStoryQ2Request,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):  
    user = openai_service.get_user(user_id=jwt_data.user_id)

    prompt = f'{input.question} : {input.answer}.\n. THIS PART IS FOR FALLING ACTION AND RESOLUTION. Culminate the story after climax and end it by providing resolution of the story. Make a meaningful and interesting ending of the story. '
    generated_story = openai_service.generate_story(user=user, answer=prompt)
    
    svc.repository.add_part_of_story(
        user_id=jwt_data.user_id, story_id=input.story_id, content=generated_story
    ) 
    
    title = openai_service.generate_title(story=generated_story)
    svc.repository.update_title(user_id=jwt_data.user_id, title=title, 
                                story_id=input.story_id)

    return CreateStoryResponse(inserted_id=input.story_id, 
                               generated_story=str(generated_story),
                               next_question="")
