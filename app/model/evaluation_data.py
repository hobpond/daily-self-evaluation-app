from pydantic import BaseModel
from uuid import uuid4
import datetime

class EvaluationData(BaseModel):
    id: str = str(uuid4())
    timestamp: datetime.datetime = datetime.datetime.utcnow()
    expectations: str
    smart_criteria: str
    communication_effectiveness: str
    team_performance: str
    feedback: str
    growth_plan: str
