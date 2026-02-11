from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
#from uuid import UUID
from sqlalchemy import func, ForeignKey
from decimal import Decimal

class Account(Base):
    '''
    This acts as the wallet of the payment system
    '''
    __tablename__ = 'accounts'
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_name: Mapped[str] = mapped_column()
    balance: Mapped[Decimal] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class TransactionLog(Base):
    '''
    Do not store any transaction but the information about the processing
    '''
    __tablename__ = 'transactionlog'
    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    reciever_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())
    amount: Mapped[Decimal] = mapped_column()
    status: Mapped[str] = mapped_column(default='pending')