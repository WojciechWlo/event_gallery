from sqlalchemy.orm import Session, joinedload
from models import Upload
from database import get_db
from fastapi.responses import StreamingResponse
from pathlib import Path
import os
from fastapi import HTTPException, BackgroundTasks

import tempfile
from config import SERVER_URL
import uuid

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
                        "mediatype": media.mediatype
                    }
                    for media in upload.media
                ]
            })

        results["last_id"] = upload_items[-1].id if upload_items else None

        return results

    finally:
        db.close()


def get_all_uploads() -> list[dict]:
    db_gen = get_db()
    db: Session = next(db_gen)

    try:
        uploads = db.query(Upload).all()
        return [
            {
                "id": upload.id,
                "nickname": upload.nickname,
                "datetime": upload.datetime.isoformat()
            }
            for upload in uploads
        ]
    finally:
        db.close()


def create_zip_from_files(file_paths: list[str], zip_path: str, base_dir: str = "media") -> None:
    import zipfile
    import os

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in file_paths:
            arcname = os.path.relpath(file, base_dir)
            print(f"Adding to zip: {file} as {arcname}")
            zipf.write(file, arcname=arcname)


def download_all_media_files() -> tuple[str, str]:
    db_gen = get_db()
    db: Session = next(db_gen)
    try:
        uploads = db.query(Upload).options(joinedload(Upload.media)).all()

        file_paths = []
        for upload in uploads:
            for media in upload.media:
                cleaned_path = media.filename.replace("\\", "/")
                if os.path.exists(cleaned_path):
                    file_paths.append(cleaned_path)

        if not file_paths:
            raise HTTPException(status_code=404, detail="No media files found in database.")

        temp_dir = tempfile.mkdtemp(prefix="zip_")
        zip_name = "media_all.zip"
        zip_path = os.path.join(temp_dir, zip_name)

        create_zip_from_files(file_paths, zip_path, base_dir="media")

        return temp_dir, zip_name

    finally:
        db.close()

def download_media_by_upload_id(upload_id: int) -> tuple[str, str]:
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
            raise HTTPException(status_code=404, detail="Upload or media not found.")

        file_paths = []
        for media in upload.media:
            cleaned_path = media.filename.replace("\\", "/")
            if os.path.exists(cleaned_path):
                file_paths.append(cleaned_path)

        if not file_paths:
            raise HTTPException(status_code=404, detail="No media files found.")

        temp_dir = tempfile.mkdtemp(prefix="zip_")
        zip_name = f"upload_{upload.id}_{upload.nickname.replace(' ', '_')}_{upload.datetime.strftime('%Y%m%d%H%M%S')}.zip"
        zip_path = os.path.join(temp_dir, zip_name)

        create_zip_from_files(file_paths, zip_path, base_dir="media")

        return temp_dir, zip_name

    finally:
        db.close()