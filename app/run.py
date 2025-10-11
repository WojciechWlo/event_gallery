from fastapi import FastAPI, Request, Depends, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from auth import authenticate_user
from fastapi.staticfiles import StaticFiles
from typing import List
from utils.savefiles import upload_files
import uvicorn
import os
import shutil
from config import EVENT_GALLERY_HOST, EVENT_GALLERY_PORT
from utils.returnfiles import get_media_after_id,\
                              download_media_by_upload_id, \
                              get_all_uploads, \
                              download_all_media_files
from config import DEBUG, APP_ENV, SSL_KEYFILE, SSL_CERTFILE
from utils.getroles import get_roles
from utils.deletefiles import delete_upload_by_id

app = FastAPI(debug=DEBUG)
templates = Jinja2Templates(directory="templates")
os.makedirs("templates", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
os.makedirs("media", exist_ok=True)
app.mount("/media", StaticFiles(directory="media"), name="media")
os.makedirs("temp", exist_ok=True)
app.mount("/temp", StaticFiles(directory="temp", html=False), name="temp")

@app.get("/", response_class=HTMLResponse)
async def gallery_page(request: Request, user: str = Depends(authenticate_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user, "roles":get_roles(user)})

@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request, user: str = Depends(authenticate_user)):
    return templates.TemplateResponse("upload.html", {"request": request, "user": user, "roles":get_roles(user)})

@app.get("/archive", response_class=HTMLResponse)
async def archive_page(request: Request, user: str = Depends(authenticate_user)):
    return templates.TemplateResponse("archive.html", {"request": request, "user": user, "roles":get_roles(user)})

@app.post("/upload-media")
async def upload_media(
    name: str = Form(...),
    files: List[UploadFile] = File(...),
    user: str = Depends(authenticate_user),
):
    urls = upload_files(files, name)

    return JSONResponse(content={"uploaded_files": urls})


@app.post("/get_uploads_with_media_part")
async def list_media_part(
    request: Request,
    user: str = Depends(authenticate_user),
):
    data = await request.json()
    upload_last_id = data.get("upload_last_id", None)
    uploads_limit = data.get("uploads_limit", 5)

    results = get_media_after_id(upload_last_id, uploads_limit)
    return JSONResponse(content=results)


@app.post("/download_media_by_upload_id")
async def download_media(
    background_tasks: BackgroundTasks,
    upload_id: int = Form(...),
    user: str = Depends(authenticate_user),
):
    try:
        temp_dir, zip_name = download_media_by_upload_id(upload_id)
        zip_path = os.path.join(temp_dir, zip_name)

        if not os.path.exists(zip_path):
            raise HTTPException(status_code=404, detail="ZIP file not created")

        background_tasks.add_task(shutil.rmtree, temp_dir)

        return FileResponse(zip_path, media_type="application/zip", filename=zip_name)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download_all_media")
async def download_all_media(
    background_tasks: BackgroundTasks,
    user: str = Depends(authenticate_user),
):
    try:
        temp_dir, zip_name = download_all_media_files()
        zip_path = os.path.join(temp_dir, zip_name)

        if not os.path.exists(zip_path):
            raise HTTPException(status_code=404, detail="ZIP file not created")

        background_tasks.add_task(shutil.rmtree, temp_dir)

        return FileResponse(zip_path, media_type="application/zip", filename=zip_name)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/list_uploads")
async def list_uploads(user: str = Depends(authenticate_user)):
    uploads_data = get_all_uploads()
    return JSONResponse(content=uploads_data)

@app.post("/delete_upload_by_id")
async def delete_upload(
    upload_id: int = Form(...),
    user: str = Depends(authenticate_user),
):
    try:
        if "admin" in get_roles(user) and delete_upload_by_id(upload_id):
            return True
        else:
            raise HTTPException(status_code=404, detail="User has not such privileges.")
            
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

if __name__ == "__main__":
    uvicorn.run("run:app",
                host=EVENT_GALLERY_HOST,
                port=EVENT_GALLERY_PORT,
                reload=APP_ENV == "development",
                ssl_keyfile=SSL_KEYFILE,
                ssl_certfile=SSL_CERTFILE)