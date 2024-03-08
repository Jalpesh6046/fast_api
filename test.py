from fastapi import HTTPException, status, Security, FastAPI
from fastapi.security import APIKeyHeader, APIKeyQuery
import pickle
from pydantic import BaseModel

API_KEYS = [
    "9d207bf0-10f5-4d8f-a479-22ff5aeff8d1",
    "f47d4a2c-24cf-4745-937e-620a5963c0b8",
    "b7061546-75e8-444b-a2c4-f19655d07eb8",
]

pickle_in = open("model.pkl", "rb")
model = pickle.load(pickle_in)

api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
) -> str:
    """Retrieve and validate an API key from the query parameters or HTTP header.

    Args:
        api_key_query: The API key passed as a query parameter.
        api_key_header: The API key passed in the HTTP header.

    Returns:
        The validated API key.

    Raises:
        HTTPException: If the API key is invalid or missing.
    """
    if api_key_query in API_KEYS:
        return api_key_query
    if api_key_header in API_KEYS:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )

app = FastAPI()

class SalaryPredictionInput(BaseModel):
    Index: float
    experience: float
    test_score: float


def predict_output(index, experience, test_score):
    prediction = model.predict([[index, experience, test_score]])
    return prediction[0]

@app.get("/public")
def public():
    """A public endpoint that does not require any authentication."""
    return "Public Endpoint"

@app.post("/private")
def private(input_data: SalaryPredictionInput, api_key: str = Security(get_api_key)):
    """A private endpoint that requires a valid API key to be provided."""
    result = predict_output(input_data.Index, input_data.experience, input_data.test_score)
    return {"predicted_salary": result}
