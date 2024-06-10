from pydantic import BaseModel
from pydantic import ConfigDict


class User(BaseModel):
    id: int
    name: str


class TagSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None


class TagCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None


class UntaggedTransactionCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    description_from_bank: str
    reference_id: str
    date: str
    value_date: str
    withdraw_amount: float
    deposit_amount: float
    closing_balance: float


class TaggedTransactionCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    description_from_bank: str
    reference_id: str
    date: str
    value_date: str
    withdraw_amount: float
    deposit_amount: float
    closing_balance: float
    tags: list[TagSchema] | None


class TransactionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description_from_bank: str
    reference_id: str
    date: str
    value_date: str
    withdraw_amount: float
    deposit_amount: float
    closing_balance: float
    tags: list[TagSchema] | None


class NotFoundResponse(BaseModel):
    message: str
