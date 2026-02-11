from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from project.logic import deposit, create_account, withdraw, transaction, get_account, get_transaction_history
from project.schemas import Deposit, Showbalance, CreateAccount, Withdraw, Transaction, TransationResponce, TransactionHistory

router = APIRouter(prefix='/api')

@router.post('/create_account', response_model=Showbalance)
async def create_new_account(task: CreateAccount, db: AsyncSession = Depends(get_db)):
    try:
        return await create_account(db, task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get('/get_one_account')
async def get_account_endpoint(account_id: int, 
                               db: AsyncSession = Depends(get_db)):
    try:
        return await get_account(db, account_id)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    

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
    
@router.post('/transaction', response_model=TransationResponce)
async def transaction_endpoint(task: Transaction,
                               db: AsyncSession = Depends(get_db)):
    try:
        return await transaction(db, task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/transaction_history', response_model=list[TransactionHistory])
async def transaction_history_endpoint(account_id: int,
                                       db: AsyncSession = Depends(get_db)):
    return await get_transaction_history(db, account_id)
