"""Auth router module."""

from fastapi import (
    APIRouter,
)
import pandas as pd
import pickle
from sklearn.feature_extraction.text import (
    TfidfVectorizer,
)
from sklearn.model_selection import (
    train_test_split,
)
from typing import (
    Any,
    Dict,
)

from app.models import (
    schemas as models_schemas,
)

router = APIRouter(prefix="/api/v1")


tfvect = TfidfVectorizer(max_features=30000, stop_words="english", max_df=0.8)
loaded_model = pickle.load(open("./notebook/model.pkl", "rb"))
true_data_pd = pd.read_csv("./notebook/data-set/DataSet_Misinfo_TRUE.csv")
true_data_pd["label"] = "real"
fake_data_pd = pd.read_csv("./notebook/data-set/DataSet_Misinfo_FAKE.csv")
fake_data_pd["label"] = "fake"
all_articles_df = pd.concat([true_data_pd, fake_data_pd], ignore_index=True)
all_articles_df.drop_duplicates(subset="text", inplace=True)
all_articles_df = all_articles_df.drop(
    all_articles_df.columns[
        all_articles_df.isna().sum() > len(all_articles_df.columns)
    ],
    axis=1,
)
all_articles_df = all_articles_df.dropna(axis=0).reset_index(drop=True)
all_articles_df.drop(columns=all_articles_df.columns[0], axis=1, inplace=True)
all_articles_df = all_articles_df.sample(10000).reset_index(drop="index")
x = all_articles_df["text"]
y = all_articles_df["label"]
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=5
)


def fake_news_classification(article: Any) -> int:
    tfvect.fit_transform(x_train)
    tfvect.transform(x_test)
    vectorized_data = tfvect.transform([article])
    prediction = loaded_model.predict(vectorized_data.toarray())
    return prediction[0]


@router.post(
    "/predict",
    response_model=models_schemas.ResponseSchema,
    status_code=200,
    name="models:predict",
    responses={
        201: {
            "model": models_schemas.ResponseSchema,
            "description": "A response object that contains the predict results.",
        },
    },
)
async def predict(
    form_data: models_schemas.MessageSchema,
) -> Dict[str, Any]:
    """
    Detect fake news.
    """
    predict = fake_news_classification(form_data.message)
    result = "fake" if predict == 0 else "real"
    return {"status_code": 200, "message": f"this article is {result}!"}
