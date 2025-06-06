from fastapi import FastAPI, Request, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from auth import authenticate_user
from fastapi.staticfiles import StaticFiles
from typing import List
from utils.savefiles import upload_files
from database import Base, engine
import uvicorn
from utils.returnfiles import get_media_after_id,\
                              download_media_by_upload_id, \
                              get_all_uploads, \
                              get_all_media_files_with_structure
from config import DEBUG, SSL_KEYFILE, SSL_CERTFILE
from create_user import create_guest_user

Base.metadata.create_all(bind=engine)

create_guest_user()

app = FastAPI(debug=DEBUG)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

@app.get("/", response_class=HTMLResponse)
async def gallery_page(request: Request, user: str = Depends(authenticate_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request, user: str = Depends(authenticate_user)):
    return templates.TemplateResponse("upload.html", {"request": request, "user": user})

@app.get("/archive", response_class=HTMLResponse)
async def archive_page(request: Request, user: str = Depends(authenticate_user)):
    return templates.TemplateResponse("archive.html", {"request": request, "user": user})

@app.post("/upload-media")
async def upload_media(
    name: str = Form(...),
    files: List[UploadFile] = File(...),  # param 'files', nie 'images'
    user: str = Depends(authenticate_user),
):
    urls = upload_files(files, name)

    return JSONResponse(content={"uploaded_files": urls})


@app.post("/get_uploads_with_media_part")
async def list_media(
    request: Request,
    user: str = Depends(authenticate_user),
):
    data = await request.json()
    upload_last_id = data.get("upload_last_id", None)
    uploads_limit = data.get("uploads_limit", 5)

    results = get_media_after_id(upload_last_id, uploads_limit)
    return JSONResponse(content=results)


@app.post("/download_media_by_upload_id")
async def list_media(
    request: Request,
    user: str = Depends(authenticate_user),
):
    data = await request.json()
    upload_id = data.get("upload_id", None)

    if not upload_id:
        return JSONResponse(content={"error": "upload_id required"}, status_code=400)

    try:
        return download_media_by_upload_id(upload_id)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/list_uploads")
async def list_uploads(user: str = Depends(authenticate_user)):
    uploads_data = get_all_uploads()
    return JSONResponse(content=uploads_data)


@app.post("/download_all_media")
async def download_all_media_with_structure(user: str = Depends(authenticate_user)):
    return get_all_media_files_with_structure()


if __name__ == "__main__":
    print("Keyfile:", SSL_KEYFILE)
    print("Certfile:", SSL_CERTFILE)
    uvicorn.run("run:app", 
                host="0.0.0.0", 
                port=8000, 
                reload=True,
                ssl_keyfile=SSL_KEYFILE,
                ssl_certfile=SSL_CERTFILE
                )