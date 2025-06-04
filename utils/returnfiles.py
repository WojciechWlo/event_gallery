from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Media
from database import get_db
import math

'''
def get_media_paginated(page_size: int = 12, page: int = 1):
    db_gen = get_db()
    db: Session = next(db_gen)

    try:
        total_count = db.query(func.count(Media.id)).scalar()
        media_items = (
            db.query(Media.filename, Media.mediatype)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
    finally:
        db_gen.close()

    total_pages = math.ceil(total_count / page_size) if page_size else 0

    return {
        "total": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "media": [
            {"filename": item.filename, "mediatype": item.mediatype.name}
            for item in media_items
        ],
    }
'''

def get_media_after_id(last_id: int | None, limit: int = 12) -> dict:
    db_gen = get_db()
    db: Session = next(db_gen)

    try:
        query = db.query(Media)

        if last_id is not None:
            query = query.filter(Media.id < last_id)

        query = query.order_by(Media.id.desc()).limit(limit)
        media_items = query.all()

        results = {
            "media": [
                {
                    "filename": item.filename,
                    "mediatype": item.mediatype.value  # np. "img" lub "video"
                }
                for item in media_items
            ],
            "last_id": media_items[-1].id if media_items else None
        }

        return results

    finally:
        db.close()