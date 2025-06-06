from fastapi import UploadFile
import os
import shutil
from datetime import datetime
from database import get_db
from sqlalchemy.orm import Session
from app.models import Upload, Media, MediaTypeEnum
from typing import List
from utils.image2webp import convert_image_to_webp
from config import SERVER_URL

def save_upload_file(upload_file: UploadFile, dest_folder: str) -> str:
    os.makedirs(dest_folder, exist_ok=True)
    file_path = os.path.join(dest_folder, upload_file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return file_path

def upload_files(files: List[UploadFile], name: str, server_url: str = SERVER_URL) -> List[str]:
    now = datetime.utcnow()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    base_path = f"./media/{timestamp}"
    urls = []

    db_gen = get_db()
    db: Session = next(db_gen)

    try:
        # Rekord Upload
        new_upload = Upload(nickname=name, datetime = now)
        db.add(new_upload)
        db.flush()  # żeby mieć dostęp do new_upload.id

        for upload_file in files:
            

            # MIME → MediaTypeEnum
            content_type = upload_file.content_type
            if content_type.startswith("image/"):
                mediatype = MediaTypeEnum.image
            elif content_type.startswith("video/"):
                mediatype = MediaTypeEnum.movie
            else:
                continue  # pomiń nieobsługiwane typy

            saved_path = save_upload_file(upload_file, base_path)

            # Konwertuj obraz do WebP, jeśli to obraz
            if mediatype == MediaTypeEnum.image:
                saved_path = convert_image_to_webp(saved_path)

            media_record = Media(
                filename=saved_path,
                mediatype=mediatype,
                upload_id=new_upload.id
            )
            db.add(media_record)

            relative_path = saved_path.replace("./", "")
            absolute_url = f"{server_url}/{relative_path}"
            urls.append(absolute_url)

        db.commit()
    finally:
        db_gen.close()

    return urls
