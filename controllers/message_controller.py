import os
import uuid
from datetime import datetime
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from database import Message
from models.schemas import MessageCreate, MessageUpdate

# Directory for storing uploaded images
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, "images")


def get_messages(db: Session):
    """
    Retrieve all messages that are not deleted.
    :param db: Database session
    :return: List of Message instances
    """
    return db.query(Message).filter(Message.deleted_at.is_(None)).all()


def create_message(db: Session, message: MessageCreate):
    """
    Create a new message in the database.
    This function takes a MessageCreate schema, creates a new Message instance,
    and saves it to the database.

    :param db: Database session
    :param message: MessageCreate schema containing the message details
    :return: The created Message instance
    """

    db_message = Message(
        title=message.title,
        category=message.category,
        text=message.text
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def update_message(db: Session, message_id: int, message: MessageUpdate):
    """
    Update an existing message in the database.
    This function retrieves a message by its ID, updates its fields if provided,
    and saves the changes to the database.
    :param db: Database session
    :param message_id: ID of the message to update
    :param message: MessageUpdate schema containing the updated fields
    :return: The updated Message instance
    """
    db_message = db.query(Message).filter(
        Message.id == message_id,
        Message.deleted_at.is_(None)
    ).first()
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")

    if message.title is not None:
        db_message.title = message.title
    if message.category is not None:
        db_message.category = message.category
    if message.text is not None:
        db_message.text = message.text
    db_message.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_message)
    return db_message


def delete_message(db: Session, message_id: int):
    """
    Soft-delete a message by setting its deleted_at timestamp.
    This function marks a message as deleted by setting the deleted_at field to the current time.
    :param db: Database session
    :param message_id: ID of the message to delete
    :raises HTTPException: If the message with the given ID does not exist
    :return: None
    """
    db_message = db.query(Message).filter(
        Message.id == message_id,
        Message.deleted_at.is_(None)
    ).first()
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")

    db_message.deleted_at = datetime.utcnow()
    db.commit()


def upload_image(db: Session, message_id: int, file: UploadFile):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ['.png', '.jpg']:
        raise HTTPException(status_code=400, detail="Invalid image format. Only PNG and JPG are allowed.")

    db_message = db.query(Message).filter(
        Message.id == message_id,
        Message.deleted_at.is_(None)
    ).first()
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")

    os.makedirs(IMAGES_DIR, exist_ok=True)
    filename = f"{uuid.uuid4()}{ext}"
    path = os.path.join(IMAGES_DIR, filename)
    with open(path, "wb") as buffer:
        buffer.write(file.file.read())

    db_message.image = filename
    db_message.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_message)
    return db_message