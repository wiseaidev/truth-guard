"""Models Schemas module."""

from pydantic import (
    BaseModel,
    Field,
)


class MessageSchema(BaseModel):
    """
    A Pydantic class that defines the article content for prediction.
    """

    message: str = Field(
        ...,
        example="A message to indicate whether the article is fake or not!",
    )


class ResponseSchema(BaseModel):
    """
    A Pydantic class that defines a Response schema object.
    """

    status_code: int = Field(
        ...,
        example=400,
    )
    message: str = Field(
        ...,
        example="A message to indicate that the request was not successful!",
    )
