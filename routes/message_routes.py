from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from controllers.message_controller import (
    get_messages, create_message, update_message,
    delete_message, upload_image
)
from database import get_db
from models.schemas import MessageCreate, MessageUpdate, MessageResponse

router = APIRouter()

# |----------------------------------------------------------------------------------
# | Messages Routes
# |----------------------------------------------------------------------------------
@router.get("/",
            summary="Message Application root",
            description="Application is running",
            tags=["home"]
            )
async def read_root():
    return {"application": "Is running"}

# |----------------------------------------------------------------------------------
# | Get all messages
# |----------------------------------------------------------------------------------
@router.get(
    "/messages",
    summary="Get all messages",
    description="Retrieve a list of all messages that are not deleted",
    response_model=list[MessageResponse],
    tags=["messages"]
)
async def read_messages(db: Session = Depends(get_db)):
    return get_messages(db)


# |----------------------------------------------------------------------------------
# | Create a new message
# |----------------------------------------------------------------------------------
@router.post(
    "/messages",
    summary="Create a new message",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["messages"]
)
async def create_new_message(
    message: MessageCreate,
    db: Session = Depends(get_db)
):
    return create_message(db, message)

# |----------------------------------------------------------------------------------
# | Upload an image for a message
# |----------------------------------------------------------------------------------

@router.post(
    "/message/upload/{message_id}",
    summary="Upload an image for a message",
    description="Upload an image file for a specific message by its ID",
    response_model=MessageResponse,
    tags=["messages"]
)
async def upload_message_img(
    message_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return upload_image(db, message_id, file)

#

@router.put(
    "/message/{message_id}",
    summary="Update an existing message",
    description="Update the details of an existing message by its ID",
    response_model=MessageResponse,
    tags=["messages"]
)
async def update_existing_message(
    message_id: int,
    message: MessageUpdate,
    db: Session = Depends(get_db)
):
    return update_message(db, message_id, message)

@router.delete(
    "/message/{message_id}",
    summary="Delete a message",
    description="Soft-delete a message by its ID",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["messages"]
)
async def delete_existing_message(
    message_id: int,
    db: Session = Depends(get_db)
):
    delete_message(db, message_id)