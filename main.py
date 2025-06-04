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

@app.post("/media")
async def list_media(
    request: Request,
    user: str = Depends(authenticate_user),
):
    data = await request.json()
    last_id = data.get("last_id", None)
    limit = data.get("limit", 12)

    results = get_media_after_id(last_id, limit)
    return JSONResponse(content=results)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)