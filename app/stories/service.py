
from app.config import database
from .repository.repository import StoriesRepository
from dotenv import load_dotenv


load_dotenv()


class Service:
    def __init__(self):
        self.repository = StoriesRepository(database)
        

def get_service():
    svc = Service()
    return svc