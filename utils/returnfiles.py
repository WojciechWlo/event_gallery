from sqlalchemy.orm import Session, joinedload
from models import Upload
from database import get_db
from fastapi.responses import StreamingResponse
import io
import zipfile
import os


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


def download_media_by_upload_id(upload_id: int) -> StreamingResponse:
    db_gen = get_db()
    db: Session = next(db_gen)

    try:
        upload = (
            db.query(Upload)
            .filter(Upload.id == upload_id)
            .options(joinedload(Upload.media))
            .first()
        )

        if not upload or not upload.media:
            raise Exception("Upload or media not found.")

        zip_buffer = io.BytesIO()

        # 🧠 Formatowanie daty: 20240605_153000
        timestamp_str = upload.datetime.strftime("%Y%m%d%H%M%S")
        safe_nickname = upload.nickname.replace(" ", "_")  # jeśli nick zawiera spacje
        filename = f"upload_{upload.id}_{safe_nickname}_{timestamp_str}.zip"

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    finally:
        db.close()