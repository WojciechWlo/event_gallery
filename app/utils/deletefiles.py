import os
from database import get_db
from sqlalchemy.orm import Session
from models import Upload, Media

def delete_upload_by_id(upload_id: int) -> bool:
    db_gen = get_db()
    db: Session = next(db_gen)

    try:
        upload = db.query(Upload).filter(Upload.id == upload_id).first()
        if not upload:
            return False

        for media in upload.media:
            if os.path.exists(media.filename):
                try:
                    os.remove(media.filename)
                except Exception as e:
                    print(f"Could not remove file {media.filename}: {e}")

        upload_folder = os.path.dirname(upload.media[0].filename) if upload.media else None
        if upload_folder and os.path.exists(upload_folder):
            try:
                os.rmdir(upload_folder)
            except OSError:
                pass

        db.delete(upload)
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        print(f"Error while removing upload {upload_id}: {e}")
        return False

    finally:
        db_gen.close()