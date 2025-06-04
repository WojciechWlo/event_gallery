from sqlalchemy.orm import Session
from models import Upload
from database import get_db

def get_media_after_id(last_id: int | None, limit: int = 5) -> dict:
    db_gen = get_db()
    db: Session = next(db_gen)

    try:
        query = db.query(Upload)

        if last_id is not None:
            query = query.filter(Upload.id < last_id)

        query = query.order_by(Upload.id.desc()).limit(limit)
        upload_items = query.all()

        results = {
            "uploads": []
        }

        for upload in upload_items:
            results["uploads"].append({
                "upload_id" : upload.id,
                "nickname" : upload.nickname,
                "datetime" : upload.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "media": [
                    {
                        "filename": media.filename,
                        "mediatype": media.mediatype.value
                    }
                    for media in upload.media
                ]
            })

        results["last_id"] = upload_items[-1].id if upload_items else None

        return results

    finally:
        db.close()