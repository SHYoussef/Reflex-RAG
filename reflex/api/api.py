from fastapi import FastAPI
from pydantic import BaseModel
from reflex.agent.interfaces.agent import IAgent

class QuestionRequest(BaseModel):
    question: str


class FastAPIendpoint:
    def __init__(self, agent: IAgent) -> None:
        self.app = FastAPI()
        self.agent = agent
        self.add_routes()

    def add_routes(self):
        @self.app.post("/generate")
        def generate_response(request: QuestionRequest):
            answer = self.agent.generate_answer(request.question)
            return {"answer": answer}