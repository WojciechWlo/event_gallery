from fastapi import FastAPI, Request, Depends, UploadFile, File, HTTPException, status, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from auth import authenticate_user
from fastapi.staticfiles import StaticFiles
from typing import List
from utils.savefiles import upload_files
from database import Base, engine
import uvicorn
#from utils.returnfiles import get_media_paginated
from utils.returnfiles import get_media_after_id
from utils.returnfiles import download_media_by_upload_id

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/gallery", response_class=HTMLResponse)
async def gallery_page(request: Request, user: str = Depends(authenticate_user)):
    return templates.TemplateResponse("gallery.html", {"request": request, "user": user})

@app.get("/upload", response_class=HTMLResponse)
async def gallery_page(request: Request, user: str = Depends(authenticate_user)):
    return templates.TemplateResponse("upload.html", {"request": request, "user": user})


@app.post("/upload-media")
async def upload_media(
    name: str = Form(...),
    files: List[UploadFile] = File(...),  # param 'files', nie 'images'
    user: str = Depends(authenticate_user),
):
    urls = upload_files(files, name)

    return JSONResponse(content={"uploaded_files": urls})

'''
@app.post("/media")
async def list_media(
    request: Request,
    user: str = Depends(authenticate_user),
):
    data = await request.json()
    page = data.get("page", 1)
    page_size = data.get("page_size", 12)

    results = get_media_paginated(page_size, page)
    return JSONResponse(content=results)
'''

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


if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)