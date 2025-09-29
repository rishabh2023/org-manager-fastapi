from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import SessionLocal
from app import crud, schemas
from app.auth import get_current_user


router = APIRouter(prefix="/organizations", tags=["organizations"])



async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/", response_model=schemas.OrgOut)
async def create_organization(
    org: schemas.OrgCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await crud.create_org(db, org, user_id=user["user_id"])

@router.get("/", response_model=list[schemas.OrgOut])
async def list_organizations(
    q: str | None = Query(None, min_length=1, max_length=100),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await crud.get_orgs(db, user_id=user["user_id"], q=q, limit=limit, offset=offset)

@router.get("/{org_id}", response_model=schemas.OrgOut)
async def get_organization(
    org_id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    org = await crud.get_org(db, org_id, user["user_id"])
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.put("/{org_id}", response_model=schemas.OrgOut)
async def update_organization(
    org_id: str,
    org: schemas.OrgUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    updated = await crud.update_org(db, org_id, org, user["user_id"])
    if not updated:
        raise HTTPException(status_code=404, detail="Organization not found or no permission")
    return updated

@router.delete("/{org_id}", status_code=204)
async def delete_organization(
    org_id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    deleted = await crud.delete_org(db, org_id, user["user_id"])
    if not deleted:
        raise HTTPException(status_code=404, detail="Organization not found or no permission")
    return
