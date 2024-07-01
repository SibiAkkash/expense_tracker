from fastapi import FastAPI, Depends, Response, status

from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy import select

from db import models
from db import SessionLocal

import schema

app = FastAPI()

# This function is injected as a dependency
# The output of yield is "injected" into the request handler
# as a function parameter
# The code in the `finally` block is run after the request handler
# This function can be thought of as a context manager for the request handlers
# __enter__() creates a session and return it
# __exit__() closes the session
def get_db_session():
    session = SessionLocal()
    print("opened db session")
    try:
        yield session
    finally:
        print("closing db session")
        session.close()


@app.get("/api/tags", response_model=list[schema.TagSchema])
def get_all_tags(session: Session = Depends(get_db_session)):
    tags = session.scalars(select(models.Tag)).all()
    return tags


@app.get("/api/transactions", response_model=list[schema.TransactionSchema])
def get_all_transactions(session: Session = Depends(get_db_session)):
    transactions = session.scalars(select(models.Transaction)).all()
    return transactions


# in this request handler, the 404 response corresponds to an error message
# and the 200 response returns the tag from the db (validated and filtered by the Tag pydantic model)
# it'll be nice if the response_model also couples the status code with the response
# this could give us type
# For example, nothing is stopping us setting status code as 404, and also returning a tag


# `response_model` validates and filters the output with that specified pydantic model
# if reponse model is Union, either of the models are user
# The `response_model` doesn't assign return types to the request handler though
# So we only get a runtime error if we return the wrong objects


@app.get(
    "/api/tag/{tag_id}", response_model=Union[schema.TagSchema, schema.NotFoundResponse]
)
# To get type errors, we'd have to add function return types like this
# Note: the function return type is models.Tag, while the response_model is schema.TagSchema
# response_model is used to validate, filter and convert the model instance to JSON
def get_tag(
    tag_id: int, response: Response, session: Session = Depends(get_db_session)
) -> models.Tag | dict[str, str]:
    tag = session.scalar(select(models.Tag).where(models.Tag.id == tag_id))

    if not tag:
        error_message = {"message": f"Tag with id = {tag_id} is not present in the db"}
        response.status_code = status.HTTP_404_NOT_FOUND
        return error_message

    # setting status code to 404 would still work, we wouldn't get any type errors
    # since we aren't associating the status code with a return type
    response.status_code = status.HTTP_200_OK
    return tag


@app.get(
    "/api/transaction/{transaction_id}",
    response_model=Union[schema.TransactionSchema, schema.NotFoundResponse],
)
def get_transaction(
    transaction_id: int, response: Response, session: Session = Depends(get_db_session)
) -> models.Transaction | dict[str, str]:
    transaction = session.scalar(
        select(models.Transaction).where(models.Transaction.id == transaction_id)
    )

    if not transaction:
        error_message = {
            "message": f"Transaction with id = {transaction_id} is not present in the db"
        }
        response.status_code = status.HTTP_404_NOT_FOUND
        return error_message

    response.status_code = status.HTTP_200_OK
    return transaction


@app.post("/api/tag", response_model=Union[schema.TagSchema, schema.NotFoundResponse])
def add_tag(
    tag: schema.TagCreateSchema,
    response: Response,
    session: Session = Depends(get_db_session),
):
    print(tag, type(tag))

    tag_in_db = session.scalar(select(models.Tag).where(models.Tag.name == tag.name))

    if tag_in_db:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Tag with name = {tag.name} already exists"}

    new_tag = models.Tag(
        name=tag.name, description=tag.description if tag.description else None
    )

    session.add(new_tag)
    session.commit()
    session.refresh(new_tag)

    return new_tag


@app.put(
    "/api/tag/{tag_id}", response_model=Union[schema.TagSchema, schema.NotFoundResponse]
)
def update_tag_name(
    tag_id: int,
    response: Response,
    tag_name: str,
    session: Session = Depends(get_db_session),
):
    tag = session.scalar(select(models.Tag).where(models.Tag.id == tag_id))

    if not tag:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Tag with id={tag_id} is not present in the db"}

    tag.name = tag_name
    session.commit()
    session.refresh(tag)

    return tag


@app.put(
    "/api/transaction/{transaction_id}",
    response_model=Union[schema.TransactionSchema, schema.NotFoundResponse],
)
def add_tag_to_transaction(
    transaction_id: int,
    response: Response,
    transaction: schema.TransactionSchema
):
    pass
