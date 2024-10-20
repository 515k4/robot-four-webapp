from pathlib import Path

import uvicorn
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient
from fastapi import FastAPI, Form, Request, status
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

account_url = "https://robotfoursbxeuw.blob.core.windows.net"
upload_container = "stblc-robot-four-upload-sbx-euw-01"
processed_container = "stblc-robot-four-processed-sbx-euw-01"


def list_processes_blobs():
    default_credential = DefaultAzureCredential()
    with BlobServiceClient(account_url, credential=default_credential) as blob_client:
        with blob_client.get_container_client(processed_container) as container_client:
            for blob in container_client.list_blobs("post_"):
                yield blob.name


def fake_upload(blob_name):
    default_credential = DefaultAzureCredential()
    with BlobServiceClient(account_url, credential=default_credential) as blob_client:
        with blob_client.get_container_client(upload_container) as container_client:
            print(f"Fake uploading {blob_name}...")
            container_client.upload_blob(blob_name, "random data", overwrite=True)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print("Request for index page received")
    blobs = list(list_processes_blobs())
    return templates.TemplateResponse(
        "index.html", {"request": request, "processes_blobs": blobs}
    )


@app.get("/favicon.ico")
async def favicon():
    file_name = "favicon.ico"
    file_path = "./static/" + file_name
    return FileResponse(
        path=file_path, headers={"mimetype": "image/vnd.microsoft.icon"}
    )


@app.post("/hello", response_class=HTMLResponse)
async def hello(request: Request, name: str = Form(...)):
    if name:
        print("Request for hello page received with name=%s" % name)
        sanitize_name = name.replace(" ", "_")[:64]
        fake_upload(sanitize_name)
        return templates.TemplateResponse(
            "hello.html", {"request": request, "name": name}
        )
    else:
        print(
            "Request for hello page received with no name or blank name -- redirecting"
        )
        return RedirectResponse(
            request.url_for("index"), status_code=status.HTTP_302_FOUND
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
