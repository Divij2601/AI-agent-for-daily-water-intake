from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent import WaterIntakeAgent 
from src.database import log_intake, get_intake_history
from src.logger import log_message

app = FastAPI()
agent = WaterIntakeAgent()

class WaterIntake(BaseModel):
    user_id: str
    intake_ml: int

app.post("/log-intake")
async def log_water_intake(request: WaterIntake):
    log_intake(request.user_id, request.intake_ml)
    analysis = agent.analyze_intake(request.intake_ml)
    log_message(f"User {request.user_id} drank {request.intake_ml} ml of water. Analysis: {analysis}")
    return {"message": "Water intake logged successfully"}

app.get("/history/{user_id}")
async def get_water_history(user_id: str):
    history = get_intake_history(user_id)
    return {"user_id": user_id, "history": history}

