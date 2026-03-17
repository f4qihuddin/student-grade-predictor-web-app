from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import os
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class StudentData(BaseModel):
    g1: int
    g2: int
    school: str
    reason: str
    higher: str
    internet: str
    romantic: str

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(__file__)

model_path = os.path.join(BASE_DIR, "../model/grade_predictor_model.pkl")

model = joblib.load(model_path)

@app.get("/")
def home():
    return {"message": "Smart Study Predictor API"}

@app.post("/predict")
def predict(data: StudentData):
    school_map = {
        "GP": 0,
        "MS": 1
    }

    higher_map = {
        "no": 0,
        "yes": 1
    }

    internet_map = {
        "no": 0,
        "yes": 1
    }

    romantic_map = {
        "no": 0,
        "yes": 1
    }

    reason_map = {
        "course" : [1, 0, 0, 0],
        "home" : [0, 1, 0, 0],
        "other" : [0, 0, 1, 0],
        "reputation" : [0, 0, 0, 1],
    }

    reason_list = reason_map[data.reason]

    features = [
        float(reason_list[0]),
        float(reason_list[1]),
        float(reason_list[2]),
        float(reason_list[3]),
        float(data.g1),
        float(data.g2),
        school_map[data.school],
        higher_map[data.higher],
        internet_map[data.internet],
        romantic_map[data.romantic]
    ]

    prediction = model.predict([features])

    return {
        "prediction": int(prediction[0])
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)