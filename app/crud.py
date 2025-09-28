from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas

async def create_org(db: AsyncSession, org: schemas.OrgCreate, user_id: str):
    db_org = models.Organization(**org.dict(), owner_user_id=user_id)
    db.add(db_org)
    await db.commit()
    await db.refresh(db_org)
    return db_org

async def get_orgs(db: AsyncSession, user_id: str):
    result = await db.execute(select(models.Organization).where(models.Organization.owner_user_id == user_id))
    return result.scalars().all()

async def get_org(db: AsyncSession, org_id: str, user_id: str):
    result = await db.execute(
        select(models.Organization).where(
            models.Organization.id == org_id,
            models.Organization.owner_user_id == user_id
        )
    )
    return result.scalars().first()

async def update_org(db: AsyncSession, org_id: str, org: schemas.OrgUpdate, user_id: str):
    stmt = (
        update(models.Organization)
        .where(models.Organization.id == org_id, models.Organization.owner_user_id == user_id)
        .values(**{k: v for k, v in org.dict(exclude_unset=True).items()})
        .returning(models.Organization)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalars().first()

async def delete_org(db: AsyncSession, org_id: str, user_id: str):
    stmt = (
        delete(models.Organization)
        .where(models.Organization.id == org_id, models.Organization.owner_user_id == user_id)
        .returning(models.Organization)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalars().first()
