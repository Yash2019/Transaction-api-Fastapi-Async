from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from project.logic import deposit, create_account, withdraw
from project.schemas import Deposit, Showbalance, CreateAccount, Withdraw

router = APIRouter(prefix='/api')

@router.post('/create_account', response_model=Showbalance)
async def create_new_account(task: CreateAccount, db: AsyncSession = Depends(get_db)):
    try:
        return await create_account(db, task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/deposit', response_model=Showbalance)
async def deposite_endpoint(task: Deposit, db: AsyncSession = Depends(get_db)):
    try:
        return await deposit(db, task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/withdraw', response_model=Showbalance)
async def withdraw_endpoint(task: Withdraw, db: AsyncSession = Depends(get_db)):
    try:
        return await withdraw(db, task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
