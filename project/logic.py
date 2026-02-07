from sqlalchemy.ext.asyncio import AsyncSession
from project.models import Account
from project.schemas import Deposit, CreateAccount, Withdraw
from sqlalchemy import select

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