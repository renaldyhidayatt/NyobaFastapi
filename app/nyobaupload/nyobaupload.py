from fastapi import UploadFile, APIRouter, File
import os
from starlette.responses import FileResponse, JSONResponse


router = APIRouter(prefix="/upload", tags=["upload"])

# path_folder = "/home/holyraven/Projects/python/fastapi/nyobafastapi"


@router.post("/")
async def uploadFile(file: UploadFile = File(...)):
    with open("media/" + file.filename, "wb") as image:
        content = await file.read()
        image.write(content)
        image.close()

    return JSONResponse(content={"filename": file.filename}, status_code=200)


@router.get("/{name_file}")
def get_file(name_file: str):
    testing_root = os.path.abspath(os.curdir)

    return FileResponse(testing_root + "/media/" + name_file)
    # file_path = os.path.join(path_folder, "media/" + name_file)

    # if os.path.exists(file_path):
    #     return FileResponse(file_path, media_type="image/png")

    # return FileResponse(getcwd() + "/app/media" + "/" + name_file)


@router.delete("/delete/file/{name_file}")
def delete_file(name_file: str):
    testing_root = os.path.abspath(os.curdir)
    try:
        os.remove(testing_root + "/media/" + name_file)
        return JSONResponse(content={"removed": True}, status_code=200)
    except FileNotFoundError:
        return JSONResponse(
            content={"removed": False, "error_message": "File not found"},
            status_code=404,
        )
