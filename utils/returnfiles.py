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
            raise Exception("Upload or media not found.")

        file_paths = [
            media.filename for media in upload.media
            if os.path.exists(media.filename)
        ]

        timestamp_str = upload.datetime.strftime("%Y%m%d%H%M%S")
        safe_nickname = upload.nickname.replace(" ", "_")
        zip_name = f"upload_{upload.id}_{safe_nickname}_{timestamp_str}.zip"

        return create_zip_response(file_paths, zip_name)

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
    base_dir = "media"

    file_paths = []
    if not os.path.exists(base_dir):
        raise Exception("Folder media nie istnieje")

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            full_path = os.path.join(root, file)
            file_paths.append(full_path)

    zip_name = f"media_all.zip"

    return create_zip_response_with_folders(base_dir, file_paths, zip_name)