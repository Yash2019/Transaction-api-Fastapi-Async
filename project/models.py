from datetime import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
    #account_id: Mapped[UUID] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    #Relationships
    sent_transaction: Mapped[List['Transaction']] = relationship(
        back_populates='sender',
        foreign_keys='[Transaction.sender_id]'
    )
    recieved_transaction: Mapped[List['Transaction']] = relationship(
        back_populates='reciever',
        foreign_keys='[Transaction.reciever_id]'
    )


class Transaction(Base):
    '''
    Do not store any transaction but the information about the processing
    '''
    __tablename__ = 'transactions'
    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    reciever_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())

    #relationship
    sender: Mapped['Account'] = relationship(
        back_populates='sent_transaction',
        foreign_keys=[sender_id]
    )
    reciever: Mapped['Account'] = relationship(
        back_populates='recieved_transaction',
        foreign_keys=[reciever_id]
    )

    #created_at: Mapped[datetime] = mapped_column(default=datetime.now)