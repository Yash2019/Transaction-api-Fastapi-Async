from pydantic import BaseModel
from decimal import Decimal

class CreateAccount(BaseModel):
    owner_name: str
    initial_deposit: Decimal | None = None

class Deposit(BaseModel):
    money: Decimal
    account_id: int

class Showbalance(BaseModel):
    id: int
    owner_name: str
    balance: Decimal

    class Config:
        from_attributes = True  # Allows Pydantic to read from SQLAlchemy models

class Withdraw(BaseModel):
    account_id: int
    money: Decimal

class Transaction(BaseModel):
    money: Decimal
    sender_id: int
    reciever_id: int

class TransationResponce(BaseModel):

    sender_id: int
    receiver_id: int
    amount: Decimal
    sender_new_balance: Decimal
    status: str

