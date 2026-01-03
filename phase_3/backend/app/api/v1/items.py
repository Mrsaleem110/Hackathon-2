from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models.item import Item as ItemModel, Priority
from app.models.user import User as UserModel
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.api.v1.auth import get_current_user

router = APIRouter()

@router.get("/items/", response_model=List[ItemRead])
async def get_items(
    skip: int = 0,
    limit: int = 100,
    owner_id: int = None,
    search: Optional[str] = None,
    completed: Optional[bool] = None,
    priority: Optional[Priority] = None,
    category: Optional[str] = None,
    sort_by: Optional[str] = "created_at",  # created_at, updated_at, due_date, priority, title
    sort_order: Optional[str] = "desc",  # asc or desc
    db: Session = Depends(get_db)
):
    query = db.query(ItemModel)

    # Apply filters
    if owner_id:
        query = query.filter(ItemModel.owner_id == owner_id)
    if search:
        query = query.filter(ItemModel.title.contains(search) | ItemModel.description.contains(search))
    if completed is not None:
        query = query.filter(ItemModel.completed == completed)
    if priority:
        query = query.filter(ItemModel.priority == priority)
    if category:
        query = query.filter(ItemModel.category == category)

    # Apply sorting
    if sort_by == "title":
        if sort_order == "asc":
            query = query.order_by(ItemModel.title.asc())
        else:
            query = query.order_by(ItemModel.title.desc())
    elif sort_by == "due_date":
        if sort_order == "asc":
            query = query.order_by(ItemModel.due_date.asc())
        else:
            query = query.order_by(ItemModel.due_date.desc())
    elif sort_by == "priority":
        if sort_order == "asc":
            query = query.order_by(ItemModel.priority.asc())
        else:
            query = query.order_by(ItemModel.priority.desc())
    elif sort_by == "updated_at":
        if sort_order == "asc":
            query = query.order_by(ItemModel.updated_at.asc())
        else:
            query = query.order_by(ItemModel.updated_at.desc())
    else:  # default to created_at
        if sort_order == "asc":
            query = query.order_by(ItemModel.created_at.asc())
        else:
            query = query.order_by(ItemModel.created_at.desc())

    items = query.offset(skip).limit(limit).all()
    return items

@router.get("/items/{item_id}", response_model=ItemRead)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return item

@router.post("/items/", response_model=ItemRead)
async def create_item(
    item: ItemCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_item = ItemModel(
        title=item.title,
        description=item.description,
        owner_id=current_user.id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/items/{item_id}", response_model=ItemRead)
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    # Only allow item owners to update their items
    if db_item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this item"
        )

    # Update item fields
    for field, value in item_update.dict(exclude_unset=True).items():
        setattr(db_item, field, value)

    db_item.updated_at = datetime.utcnow()  # Update timestamp
    db.commit()
    db.refresh(db_item)
    return db_item


@router.patch("/items/{item_id}/toggle-completed", response_model=ItemRead)
async def toggle_item_completed(
    item_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    # Only allow item owners to update their items
    if db_item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this item"
        )

    # Toggle the completion status
    db_item.completed = not db_item.completed
    db_item.updated_at = datetime.utcnow()  # Update timestamp

    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/items/{item_id}")
async def delete_item(
    item_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    # Only allow item owners to delete their items
    if db_item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this item"
        )

    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}

@router.get("/users/{user_id}/items", response_model=List[ItemRead])
async def get_user_items(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    completed: Optional[bool] = None,
    priority: Optional[Priority] = None,
    category: Optional[str] = None,
    sort_by: Optional[str] = "created_at",  # created_at, updated_at, due_date, priority, title
    sort_order: Optional[str] = "desc",  # asc or desc
    db: Session = Depends(get_db)
):
    query = db.query(ItemModel).filter(ItemModel.owner_id == user_id)

    # Apply filters
    if search:
        query = query.filter(ItemModel.title.contains(search) | ItemModel.description.contains(search))
    if completed is not None:
        query = query.filter(ItemModel.completed == completed)
    if priority:
        query = query.filter(ItemModel.priority == priority)
    if category:
        query = query.filter(ItemModel.category == category)

    # Apply sorting
    if sort_by == "title":
        if sort_order == "asc":
            query = query.order_by(ItemModel.title.asc())
        else:
            query = query.order_by(ItemModel.title.desc())
    elif sort_by == "due_date":
        if sort_order == "asc":
            query = query.order_by(ItemModel.due_date.asc())
        else:
            query = query.order_by(ItemModel.due_date.desc())
    elif sort_by == "priority":
        if sort_order == "asc":
            query = query.order_by(ItemModel.priority.asc())
        else:
            query = query.order_by(ItemModel.priority.desc())
    elif sort_by == "updated_at":
        if sort_order == "asc":
            query = query.order_by(ItemModel.updated_at.asc())
        else:
            query = query.order_by(ItemModel.updated_at.desc())
    else:  # default to created_at
        if sort_order == "asc":
            query = query.order_by(ItemModel.created_at.asc())
        else:
            query = query.order_by(ItemModel.created_at.desc())

    items = query.offset(skip).limit(limit).all()
    return items