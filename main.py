from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Task 1: Load the best model from Lab 2
model = joblib.load("model.pkl")

# Define the input format based on Wine Quality features
class WineFeatures(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

@app.post("/predict")
async def predict(features: WineFeatures):
    # Convert input to DataFrame for the model
    data = pd.DataFrame([features.dict().values()], 
                        columns=features.dict().keys())
    
    prediction = model.predict(data)
    
    # Task 2: Required Response Format
    return {
        "name": "Abel Philip Joseph",
        "roll_no": "2022bcs0068",
        "wine_quality": float(prediction[0])
    }
