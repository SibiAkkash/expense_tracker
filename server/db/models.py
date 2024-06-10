from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, ForeignKey, Column

from typing import List, Optional


class Base(DeclarativeBase):
    pass


transaction_tag_association_table = Table(
    "transaction_tag",
    Base.metadata,
    Column(
        "transaction_id",
        ForeignKey("bank_transaction.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("tag_id", ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
)


class Transaction(Base):
    # https://www.sqlite.org/lang_keywords.html
    # transaction is a reserved name in sqlite
    __tablename__ = "bank_transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    description_from_bank: Mapped[str]  # UPI - sender name - sender details etc..
    reference_id: Mapped[str]  # transaction reference id from the bank
    date: Mapped[str]
    value_date: Mapped[str]
    withdraw_amount: Mapped[float] = mapped_column(insert_default=0.0)
    deposit_amount: Mapped[float] = mapped_column(insert_default=0.0)
    closing_balance: Mapped[float] = mapped_column()

    # https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#declarative-vs-imperative-forms
    # the relationship() construct is deriving the target class and collection type
    # from the Mapped annotation
    # the corresponding non-annotated form should use the desired class,
    # or string class name, as the first argument passed to relationship()

    tags: Mapped[Optional[List["Tag"]]] = relationship(
        secondary=transaction_tag_association_table
    )

    def __repr__(self) -> str:
        return f"""
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
        """


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]

    def __repr__(self):
        return f"Tag(id={self.id}, name={self.name})"