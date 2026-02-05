from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from project.logic import deposit, create_account
from project.schemas import Deposit, Showbalance, CreateAccount

router = APIRouter(prefix='/api')

@router.post('/create_account', response_model=Showbalance)
async def create_new_account(task: CreateAccount,
                             db: AsyncSession = Depends(get_db)):
    return await create_account(db, task)
    

@router.post('/deposit', response_model=Showbalance)
async def deposite_endpoint(task: Deposit, db: AsyncSession = Depends(get_db)):
    return await deposit(db, task)