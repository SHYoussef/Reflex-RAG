from abc import ABC, abstractmethod


class IAgent(ABC):

    @abstractmethod
    def generate_answer(self, question: str) -> str:
        pass
