from typing import Any
import openai
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


class OpenAIService:
    def __init__(self, api_key: str):
        openai.api_key = api_key

        self.users = []
        
        self.model = ChatOpenAI(
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
            openai_api_key=openai.api_key,
            model="gpt-3.5-turbo-0613",
            temperature=0.7,
            max_tokens=900,
        )

        self.question_model = ChatOpenAI(
            streaming=True,
            openai_api_key=openai.api_key,
            model="gpt-3.5-turbo-0613",
            temperature=0.7,
            max_tokens=100,
        )

        self.title_model = ChatOpenAI(
            streaming=True,
            openai_api_key=openai.api_key,
            model="gpt-3.5-turbo-0613",
            temperature=0.7,
            max_tokens=20,
        )

        self.story_template = """
                You are J.K. Rowling.
                Be close to J.K. Rowlinge’s style of writing.
                Generate a part of the story of the Harry Potter universe based on its 
                previous parts: {chat_history}
                User's input: {answer} 
                The user will give the part of a story 
                and answer to the question. 
                (STRICT) ONLY GENERATE one part of the story.
                in one go based on the answer to the question.
                Return the story in a single paragraph and do not divide it into multiple paragraphs.
                In the text, do not address the reader!!!
                Don't write : "the stage was sent for the next chapter in 
                the magical saga of Hogwarts"!!!!!!!
                (STRICT) DON'T REPEAT the previous parts of the story!!!!!
        """

        self.title_template = """
            You are J.K. Rowling.
            Be close to J.K. Rowlinge’s style of writing.
            You need to creare a title for  a story based on its ending: {story}
            No more than 5 words in each story
        """

        self.title_prompt = PromptTemplate(
            input_variables=['story'], template=self.title_template
        )

        self.title_chain = LLMChain(
            llm=self.title_model,
            verbose=True,
            prompt=self.title_prompt
        )

        # self.question_template = " Generate a question that will develop an interesting story part for {story_part} with the main characters Leila in the Harry Potter universe. Do not ask questions similar to these ones: {question_history}. ASK ONLY ONE QUESTION Do not add to the question \"What if\", make the questions simple and interesting that fit the text"

    def generate_story(self, user: dict, answer: str) -> str:
        return user['llm_chain'].predict(answer=answer)
        # return self.llm_chain.predict(answer=answer)
    
    def generate_question(self, user: dict, story_part: str) -> str:
        # return user['characters']
        # print(user['characters'])
        return user['question_chain'].predict(story_part=story_part)
    
    def create_user(self, user_id, characters):
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        prompt = PromptTemplate(
            input_variables=["chat_history", "answer"], template=self.story_template
        )

        llm_chain = LLMChain(
            llm=self.model,
            verbose=True,
            memory=memory,
            prompt=prompt,
        )

        questions_memory = ConversationBufferMemory(memory_key="question_history", return_messages=True)
        qtemplate = " Generate a question that will develop an interesting story part for {story_part} with the main characters " + characters +" in the Harry Potter universe. Do not ask questions similar to these ones: {question_history}. ASK ONLY ONE QUESTION Do not add to the question \"What if\", make the questions simple and interesting that fit the text"
        question_prompt = PromptTemplate(
            input_variables=["question_history", "story_part"], template=qtemplate
        )

        question_chain = LLMChain(
            llm=self.question_model,
            verbose=True,
            prompt=question_prompt,
            memory=questions_memory
        )

        new_user = {
            'user_id': user_id,
            'memory': memory,
            'llm_chain': llm_chain,
            'question_memory': questions_memory,
            'question_chain': question_chain,
        }
        self.users.append(new_user)
        return new_user
    
    def get_user(self, user_id):
        for user in reversed(self.users):
            if user['user_id'] == user_id:
                return user
        return None


    def generate_title(self, story):
        return self.title_chain.predict(story=story)
        





        
    
