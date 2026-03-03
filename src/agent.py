import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5,
)

class WaterIntakeAgent:
    
    def __init__(self):
        self.history = []

    def analyze_intake(self, intake_ml):

        prompt= f"""
        You are a hydration assistant. The user has consumed {intake_ml} ml of water today. Proide a hydration status and check if they need to drink more water.
        the response should be in a single sentence, comprising of all the information within 100 words.
        """
        response= llm.invoke([HumanMessage(content=prompt)])

        return response.content

if __name__== "__main__":
    agent=WaterIntakeAgent()
    intake=1500
    feedback = agent.analyze_intake(intake)
    print(f"Hydration Analysis: {feedback}")



