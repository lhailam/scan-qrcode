from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os

from reader_qr import qr_code_reader


class ImagePathPayload(BaseModel):
    path: str


class FolderPathPayload(BaseModel):
    folder_path: str


app = FastAPI(title="QR Scan API")


IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")



@app.get("/health-check")
def health_check() -> Dict[str, Any]:
    return {"status": "ok"}

@app.post("/scan-image")
def scan_image(payload: ImagePathPayload) -> Dict[str, Optional[str]]:
    path = payload.path
    if not os.path.isfile(path):
        return {"data": None}

    if not path.lower().endswith(IMAGE_EXTENSIONS):
        return {"data": None}

    result = qr_code_reader(path)
    if isinstance(result, str) and (result.startswith("Error:") or result == "Không thể đọc file ảnh" or result == "Không thể giải mã QR code"):
        return {"data": None}

    return {"data": result if isinstance(result, str) else None}


@app.post("/scan-folder")
def scan_folder(payload: FolderPathPayload) -> Dict[str, Any]:
    folder_path = payload.folder_path
    if not os.path.isdir(folder_path):
        return {"results": {}}

    results: Dict[str, Optional[str]] = {}

    # Process files sequentially
    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith(IMAGE_EXTENSIONS):
            file_path = os.path.join(folder_path, filename)
            result = qr_code_reader(file_path)
            if isinstance(result, str) and (result.startswith("Error:") or result == "Không thể đọc file ảnh" or result == "Không thể giải mã QR code"):
                results[filename] = None
            else:
                results[filename] = result if isinstance(result, str) else None

    return {"results": results}


# To run: uvicorn api_server:app --host 0.0.0.0 --port 8000


