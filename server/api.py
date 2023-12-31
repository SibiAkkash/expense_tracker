from fastapi import FastAPI, Depends, Response, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

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
    print('opened db session')
    try:
        yield session
    finally:
        print('closing db session')
        session.close()


@app.get('/api/tags', response_model=list[schema.TagSchema])
def get_all_tags(session: Session = Depends(get_db_session)):
    tags = session.scalars(select(models.Tag)).all()
    return tags


@app.get('/api/transactions', response_model=list[schema.TransactionSchema])
def get_all_transactions(session: Session = Depends(get_db_session)):
    transactions = session.scalars(select(models.Transaction)).all()
    return transactions



'''
    * By specifiying response_model as Union of 2 pydantic models, 
    * the returned object is validated against either of these 2 models
    * if the return value matches any of the return types, the return value if modified
    * according to the schema specified in the pydantic model
    
    * in this request handler, the 404 response corresponds to an error message
    * and the 200 response returns the tag from the db (validated and filtered by the Tag pydantic model)
    
    * it'll be nice if the response_model also couples the status code with the response
    * this could give us type
    * For example, nothing is stopping us setting status code as 404, and also returning a tag
'''

@app.get('/api/tag/{tag_id}', response_model = Union[schema.TagSchema, schema.NotFoundResponse])
def get_tag(
        tag_id: int, 
        response: Response, 
        session: Session = Depends(get_db_session)
    ) -> models.Tag | dict[str, str]:
    
    tag = session.scalar(select(models.Tag).where(models.Tag.id == tag_id))
    
    if not tag:
        error_message = {"message": f"Tag with id={tag_id} is not present in the db"}
        response.status_code = status.HTTP_404_NOT_FOUND
        return error_message
    
    # setting status code to 404 would still work, we wouldn't get any type errors
    response.status_code = status.HTTP_200_OK
    return tag
        
        

@app.post('/api/tags', response_model=schema.TagSchema)
def add_tag(session: Session = Depends(get_db_session)):
    pass


@app.put('/api/tag/{tag_id}', response_model=Union[schema.TagSchema, schema.NotFoundResponse])
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
    
    
