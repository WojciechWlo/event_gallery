from sqlalchemy.orm import Session, joinedload
from models import Upload
from database import get_db
from fastapi.responses import StreamingResponse
import io
import zipfile
import os
from fastapi import HTTPException


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

def create_zip_response(file_paths: list[str], zip_name: str) -> StreamingResponse:
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in file_paths:
            arcname = os.path.basename(file_path)
            zip_file.write(file_path, arcname=arcname)

    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={zip_name}"}
    )


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
            raise HTTPException(status_code=404, detail="Upload or media not found.")

        file_paths = []
        for media in upload.media:
            # Zamiana backslash na slash, żeby działało w Linux/Docker
            cleaned_path = media.filename.replace("\\", "/")

            # Jeśli ścieżka jest względna względem /app (wewnątrz kontenera), nie dodawaj /app
            if os.path.exists(cleaned_path):
                file_paths.append(cleaned_path)

        if not file_paths:
            raise HTTPException(status_code=404, detail="No media files found on disk for this upload.")

        # Ustawiamy base_dir na katalog 'media', żeby zachować strukturę z rodzicem
        base_dir = "media"

        timestamp_str = upload.datetime.strftime("%Y%m%d%H%M%S")
        safe_nickname = upload.nickname.replace(" ", "_")
        zip_name = f"upload_{upload.id}_{safe_nickname}_{timestamp_str}.zip"

        return create_zip_response_with_folders(base_dir, file_paths, zip_name)

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


def create_zip_response_with_folders(base_dir: str, file_paths: list[str], zip_name: str) -> StreamingResponse:
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in file_paths:
            # zachowujemy ścieżkę względem base_dir
            arcname = os.path.relpath(file_path, base_dir)
            zip_file.write(file_path, arcname=arcname)

    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={zip_name}"}
    )

def create_zip_response_with_folders(base_dir: str, file_paths: list[str], zip_name: str) -> StreamingResponse:
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in file_paths:
            arcname = os.path.relpath(file_path, base_dir)
            zip_file.write(file_path, arcname=arcname)

    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={zip_name}"}
    )


def get_all_media_files_with_structure() -> StreamingResponse:
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

        base_dir = os.path.commonpath(file_paths)

        zip_name = "media_all.zip"

        return create_zip_response_with_folders(base_dir, file_paths, zip_name)

    finally:
        db.close()