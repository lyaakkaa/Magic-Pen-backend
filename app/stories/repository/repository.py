from typing import Any
from datetime import datetime
from bson.objectid import ObjectId
from pymongo.database import Database


class StoriesRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_story(self, user_id: str, content: str, title: str):
        payload = {
            "title": title,
            "content": content,
            "user_id": ObjectId(user_id),
        }

        insert_result = self.database["stories"].insert_one(payload)
        return insert_result.inserted_id
    
    def add_part_of_story(self, user_id: str, story_id: str, content: str):
        prev_story = self.database["stories"].find_one(
            {"user_id": ObjectId(user_id), "_id": ObjectId(story_id)}
        )
        print(prev_story['content'])

        if prev_story is None:
            return None
       
        return self.database["stories"].update_one(
            filter={"user_id": ObjectId(user_id), "_id": ObjectId(story_id)},
            update={
                "$set": {
                    "content": prev_story['content'] + " " + content
                },
            },
        )
    
    def get_previous_story(self, user_id: str, story_id: str):
        prev_story = self.database["stories"].find_one(
            {"user_id": ObjectId(user_id), "_id": ObjectId(story_id)}
        )
        return prev_story['content']
    
    def get_story(self, user_id: str, story_id: str):
        story = self.database["stories"].find_one(
            filter={"user_id": ObjectId(user_id), "_id": ObjectId(story_id)},
        )
        return story
    
    def delete_story(self, story_id: str, user_id: str):
        return self.database["stories"].delete_one(
            {"_id": ObjectId(story_id), "user_id": ObjectId(user_id)}
        )
    
    def get_stories(self, user_id: str):
        stories = self.database["stories"].find(
            filter={"user_id": ObjectId(user_id)}
        )
        return list(stories)
    
    def update_title(self, user_id: str, story_id: str, title: str):
        self.database["stories"].update_one(
            filter={"user_id": ObjectId(user_id), "_id": ObjectId(story_id)},
            update={
                "$set": {
                    "title": title
                },
            },
        )

    