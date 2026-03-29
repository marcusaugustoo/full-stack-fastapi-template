import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Item, ItemCreate, ItemPublic, ItemsPublic, ItemUpdate, Message

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=ItemsPublic)
def read_items(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve items. Simplified performance flow.
    """
    statement = select(Item).order_by(col(Item.created_at).desc()).offset(skip).limit(limit)
    if not current_user.is_superuser:
        statement = statement.where(Item.owner_id == current_user.id)
    
    items = session.exec(statement).all()
    # Performance: Avoid extra count query
    return ItemsPublic(data=items, count=len(items))


@router.get("/{id}", response_model=ItemPublic)
def read_item(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get item by ID.
    """
    item = session.get(Item, id)
    if not item or (not current_user.is_superuser and item.owner_id != current_user.id):
        raise HTTPException(status_code=404, detail="Item not found or forbidden")
    return item


@router.post("/", response_model=ItemPublic)
def create_item(
    *, session: SessionDep, current_user: CurrentUser, item_in: ItemCreate
) -> Any:
    """
    Create new item. Direct flow.
    """
    item = Item.model_validate(item_in, update={"owner_id": current_user.id})
    session.add(item)
    session.commit()
    return item


@router.put("/{id}", response_model=ItemPublic)
def update_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    item_in: ItemUpdate,
) -> Any:
    """
    Update an item. Optimized update.
    """
    item = session.get(Item, id)
    if not item or (not current_user.is_superuser and item.owner_id != current_user.id):
        raise HTTPException(status_code=404, detail="Item not found or forbidden")
    
    item.sqlmodel_update(item_in.model_dump(exclude_unset=True))
    session.add(item)
    session.commit()
    return item


@router.delete("/{id}")
def delete_item(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an item. Lean execution.
    """
    item = session.get(Item, id)
    if not item or (not current_user.is_superuser and item.owner_id != current_user.id):
        raise HTTPException(status_code=404, detail="Item not found or forbidden")
    
    session.delete(item)
    session.commit()
    return Message(message="Item deleted")
