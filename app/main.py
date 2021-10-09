from fastapi import FastAPI
from config.database import engine
from fastapi_jwt_auth import AuthJWT
from starlette.staticfiles import StaticFiles

from blog import blogrouter, models as blogmodels
from comment import commentrouter, models as commentmodels
from nyobaupload import nyobaupload
from users import usersrouter, models as usersmodels
from auth import authrouter, schema


app = FastAPI()


blogmodels.Base.metadata.create_all(bind=engine)
commentmodels.Base.metadata.create_all(bind=engine)
usersmodels.Base.metadata.create_all(bind=engine)


@AuthJWT.load_config
def get_config():
    return schema.Settings()


# app.mount("/media", StaticFiles(directory="media"))


@app.get("/")
def hello():
    return "Hello"


app.include_router(blogrouter.router)
app.include_router(commentrouter.router)
app.include_router(authrouter.router)
app.include_router(usersrouter.router)
# app.include_router(nyobaupload.router)
