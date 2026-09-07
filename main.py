from fastapi import FastAPI
from pydantic import BaseModel, field_validator
import joblib
import pandas as pd
from scipy.sparse import hstack

app = FastAPI()

NBmodel = joblib.load("models/ComplementNB.pkl")
Svcmodel = joblib.load("models/LinierSVC.pkl")
Logisticmodel = joblib.load("models/LogisticRegression.pkl")

raw_encoders = joblib.load("encoder/encoders.joblib")
target_encoder = next(e for e in raw_encoders if type(e).__name__ == "TargetEncoder")
label_encoder = next(e for e in raw_encoders if type(e).__name__ == "LabelEncoder")
tfidf_encoders = [e for e in raw_encoders if type(e).__name__ == "TfidfVectorizer"]

tfidf_encoders.sort(key=lambda vec: vec.idf_[vec.vocabulary_.get("photos", 0)])
headline_encoder = tfidf_encoders[0]
desc_encoder = tfidf_encoders[1]


class InputData(BaseModel):
    headline: str
    short_description: str
    authors: str = ""
    link: str = ""
    category: str = ""
    date: str = ""

    @field_validator("headline", "short_description")
    @classmethod
    def check_min_length(cls, value: str):
        if len(value.strip()) <= 3:
            raise ValueError("Provide at least 3 characters")
        return value


def encode(data: InputData):
    df_authors = pd.DataFrame([[data.authors]], columns=["authors"])
    authors_encoded = target_encoder.transform(df_authors)
    headline_encoded = headline_encoder.transform([data.headline])
    desc_encoded = desc_encoder.transform([data.short_description])

    return hstack([headline_encoded, desc_encoded, authors_encoded])


@app.get("/")
def home():
    return {
        "System MSG:": "News Categorization API is Online",
        "Live At:": "https://nac-api-opmx.onrender.com",
        "Interactive UI:": "https://nac-api-opmx.onrender.com/docs",
        "Test Inputs:": "https://docs.google.com/document/d/1PNjAmppqH00A_i8AZWuJq_umSun2_RqFHjDBRuNn7Rg/edit?usp=sharing",
    }

@app.get("/health")
async def health():
    return {"status": "ok"}



@app.post("/predict")
def predict(data: InputData):
    features = encode(data)

    nb_pred = NBmodel.predict(features)[0]
    svc_pred = Svcmodel.predict(features)[0]
    logistic_pred = Logisticmodel.predict(features)[0]

    return {
        "NaiveByes prediction": label_encoder.classes_[nb_pred],
        "Linier Svc prediction": label_encoder.classes_[svc_pred],
        "Logistic Regression prediction": label_encoder.classes_[logistic_pred],
    }

        
    
