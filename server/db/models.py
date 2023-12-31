from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List, Optional

class Base(DeclarativeBase): 
    pass

class Transaction(Base):
    __tablename__ = "transactions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    reference_id: Mapped[int]
    date: Mapped[str]
    withdraw_amount: Mapped[float] = mapped_column(insert_default=0.0)
    deposit_amount: Mapped[float] = mapped_column(insert_default=0.0)
    closing_balance: Mapped[float] = mapped_column()
    
    
class Tag(Base):
    __tablename__ = "tags"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    
    def __repr__(self):
        return f"Tag(id={self.id}, name={self.name})"