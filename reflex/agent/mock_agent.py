from reflex.agent.interfaces.agent import IAgent


class MockAgent(IAgent):

    def generate_answer(self, question: str) -> str:
        return f"Agent's answer to: {question}"
  