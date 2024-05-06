import time
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from operations.models import Operation
from database import get_async_session
from sqlalchemy import select, insert
from operations.schemas import OperationCreate
from fastapi_cache.decorator import cache


router = APIRouter(prefix="/operations", tags=["Operation"])


@router.get("/")
async def get_specific_operation(
    operation_type: str, session: AsyncSession = Depends(get_async_session)
):
    query = select(Operation).where(Operation.type == operation_type)
    result = await session.execute(query)
    operations = result.scalars().all()
    return jsonable_encoder([operation.__dict__ for operation in operations])


@router.post("/")
async def add_specific_operation(
    new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(Operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/long_operation")
@cache(expire=30)
async def get_long_op():
    time.sleep(2)
    return "Что-то пошло"
