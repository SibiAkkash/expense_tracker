from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List, Optional

class Base(DeclarativeBase): 
    pass

class Transaction(Base):
    __tablename__ = "transactions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    description_from_bank: Mapped[str] # UPI - sender name - sender details etc..
    reference_id: Mapped[int] # transaction reference id from the bank
    date: Mapped[str]
    value_date: Mapped[str]
    withdraw_amount: Mapped[float] = mapped_column(insert_default=0.0)
    deposit_amount: Mapped[float] = mapped_column(insert_default=0.0)
    closing_balance: Mapped[float] = mapped_column()
    
    # tags: Mapped[Optional[List["Tag"]]]
    
    def __repr__(self) -> str:
        return f'''
            Transaction (
                id: {self.id}
                description_from_bank: {self.description_from_bank}
                reference_id: {self.reference_id}
                date: {self.date}
                value_date: {self.value_date}
                withdraw_amount: {self.withdraw_amount}
                deposit_amount: {self.deposit_amount}
                closing_balance: {self.closing_balance}
            )
        '''
    
    
class Tag(Base):
    __tablename__ = "tags"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    
    def __repr__(self):
        return f"Tag(id={self.id}, name={self.name})"