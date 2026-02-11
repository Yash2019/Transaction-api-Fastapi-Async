from sqlalchemy.ext.asyncio import AsyncSession
from project.models import Account, TransactionLog
from project.schemas import Deposit, CreateAccount, Withdraw, Transaction
from sqlalchemy import select, or_

async def create_account(db: AsyncSession,
                         task: CreateAccount):
    
    if task.initial_deposit is not None and task.initial_deposit<=0:
        raise ValueError("Initial amount should be legal")
    
    new_account = Account(
        owner_name = task.owner_name,
        balance = task.initial_deposit or 0
    )
    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)
    return new_account

async def get_account(db: AsyncSession, account_id: int):
    stmt = select(Account).where(Account.id == account_id)
    result = await db.execute(stmt)
    account = result.scalars().first()

    if account:
        return account
    raise ValueError('Account not found')


async def deposit(db: AsyncSession, task:Deposit):
    if task.money<=0:
        raise ValueError('Amount should be Legal')

    stmt = select(Account).where(Account.id == task.account_id).with_for_update()
    result = await db.execute(stmt)
    account = result.scalars().first()

    if not account:
        raise ValueError("Account not found")
    
    account.balance+= task.money
    await db.commit()
    await db.refresh(account)
    return account


async def withdraw(db: AsyncSession, task:Withdraw):

    stmt = select(Account).where(Account.id == task.account_id).with_for_update()
    result = await db.execute(stmt)
    account = result.scalars().first()

    if not account:
        raise ValueError('Account not found')
    
    if task.money<=0:
        raise ValueError('Cannot witdraw 0 or negative amount')
    
    if task.money>account.balance:
        raise ValueError('Cannot withdraw amount more the the account balance accout')
    
    account.balance-=task.money

    await db.commit()
    await db.refresh(account)
    return account

async def transaction(db: AsyncSession, task: Transaction):
    stmt = select(Account).where(Account.id == task.sender_id).with_for_update()
    result = await db.execute(stmt)
    sender_account = result.scalars().first()

    stmt = select(Account).where(Account.id == task.reciever_id).with_for_update()
    result = await db.execute(stmt)
    reciever_account = result.scalars().first()

    if not sender_account:
        raise ValueError('Your account was not found create it')
    
    if not reciever_account:
        raise ValueError('Reciever account does not exists')
    
    if task.money<=0:
        raise ValueError('Money cannot be negative or zero')
    
    if task.sender_id == task.reciever_id: 
        raise ValueError('Cannot transfer to same account')
    
    if task.money>sender_account.balance:
        raise ValueError('Less money in the account')
    
    sender_account.balance-=task.money

    reciever_account.balance+=task.money

    log = TransactionLog(
        sender_id=sender_account.id,
        reciever_id=reciever_account.id,
        amount=task.money,
        status='complete'

    )
    db.add(log)
    await db.commit()
    await db.refresh(sender_account)
    await db.refresh(reciever_account)

    return {
        "sender_id": task.sender_id,
        "receiver_id": task.reciever_id,
        "amount": task.money,
        "sender_new_balance": sender_account.balance,
        "status": "success"
    }

async def get_transaction_history(db: AsyncSession, account_id:int):
    stmt = select(TransactionLog).where(or_(
        TransactionLog.sender_id == account_id,
        TransactionLog.reciever_id == account_id
    ))
    result = await db.execute(stmt)
    logs = result.scalars().all()
    return logs







