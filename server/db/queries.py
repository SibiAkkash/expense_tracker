from sqlalchemy import select, inspect, delete
from sqlalchemy.orm import Session
from .models import Tag

def read_all_tags(session: Session):
    all_tags = session.scalars(select(Tag)).all()
    return all_tags


def delete_all_tags(session: Session):
    session.execute(delete(Tag).where(Tag.name.in_(["Petrol", "Groceries", "Clothes"]))) 
    session.commit()       
    

def add_tag(session: Session, tag_name: str) -> Tag:
    tag = Tag(name=tag_name)
    session.add(tag)
    session.commit()
    # objects are expired on commit
    session.refresh(tag)    

    return tag

def update_tag_name(session: Session, tag_id: int, new_tag_name: str):
    tag = session.scalar(
        select(Tag)
        .where(Tag.id == tag_id)
    )
    
    if not tag:
        return {"error": "Tag not found"}
    
    tag.name = new_tag_name
    session.commit()
    return tag