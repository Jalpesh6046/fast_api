from fastapi import FastAPI
import pickle
from pydantic import BaseModel

pickle_in = open("model.pkl", "rb")
model = pickle.load(pickle_in)

app = FastAPI()

class SalaryPredictionInput(BaseModel):
    Index: float
    experience: float
    test_score: float

def predict_output(index, experience, test_score):
    prediction = model.predict([[index, experience, test_score]])
    return prediction[0] 

@app.post("/predict")
def predict(input_data: SalaryPredictionInput):
    """Endpoint to predict salary based on input data."""
    result = predict_output(input_data.Index, input_data.experience, input_data.test_score)
    return {"predicted_salary": result}
