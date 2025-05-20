from typing import Optional

import uvicorn
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Query, Path, FastAPI
from fastapi.responses import JSONResponse, HTMLResponse, ORJSONResponse, UJSONResponse
from fastapi.encoders import jsonable_encoder
from json import dumps, loads, JSONEncoder

from odmantic import Model
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from config.db import create_db_engine, create_db_connection, close_db_connection
from session_sample.models.dto import LoginReq, ProfileReq
from session_sample.models.models import Profile
from session_sample.repo.login import LoginRepository
from session_sample.repo.session import DbSessionRepository
from util.json_date import json_datetime_serializer
from util.auth_session import get_current_user, secret_key, SessionDbMiddleware
from jose import jwt
from cryptography.fernet import Fernet
import json

key = Fernet.generate_key()

from bson import ObjectId

from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")



class JSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)



@router.post("/login/authenticate")
async def authenticate(response: Response,
                       username: str = Query(..., description='The username of the credentials.', max_length=50),
                       password:
                       str = Query(..., description='The password of the of the credentials.', max_length=20),
                       engine=Depends(create_db_engine)):
    repo: LoginRepository = LoginRepository(engine)
    login = await repo.get_login_credentials(username, password)
    if login == None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication"
        )
    token = jwt.encode({"sub": username}, secret_key)
    response.set_cookie("session", token)
    return {"username": username}


@router.post("/login/add")
async def add_login(req: LoginReq, engine=Depends(create_db_engine)):
    """
    {
       login_id: int
    username: str
    password: str
    }
    """
    login_dict = req.model_dump(exclude_unset=True)
    repo: LoginRepository = LoginRepository(engine)
    result = await repo.insert_login(login_dict)
    if result == True:
        return req
    else:
        return JSONResponse(content={"message": "insert login unsuccessful"}, status_code=500)


@router.post("/login/profile/add")
async def add_login_profile(req: ProfileReq, username: str, engine=Depends(create_db_engine),
                            user: str = Depends(get_current_user)):
    """
    {
        "firstname": "hello",
        "lastname": "good",
        "middlename": "gim",
        "date_signed": "2025-12-12 12:23:43",
        "age": 34,
        "occupation": "worker",
        "birthday": "2012-09-12",
        "address": "street no. 1"
    }
    """
    profile_dict = req.model_dump(exclude_unset=True)
    profile_json = dumps(profile_dict, default=json_datetime_serializer)
    repo: LoginRepository = LoginRepository(engine)
    result = await repo.add_profile(loads(profile_json), username)
    if result:
        return req
    else:
        return JSONResponse(content={"message": "insert purchase unsuccessful"}, status_code=500)


@router.get("/login/list/all")
async def list_all_login(engine=Depends(create_db_engine), user: str = Depends(get_current_user)):
    repo: LoginRepository = LoginRepository(engine)
    result = await repo.get_all_login()
    return ORJSONResponse(content=jsonable_encoder(result), status_code=201)


@router.get("/login/account/{id}")
async def get_login(id: int = Path(..., description="The user ID of the user."), engine=Depends(create_db_engine),
                    user: str = Depends(get_current_user)):
    repo: LoginRepository = LoginRepository(engine)
    result = await repo.get_login_id(id)
    return UJSONResponse(content=jsonable_encoder(result), status_code=201)


@router.get("/logout")
async def logout(response: Response, engine=Depends(create_db_engine), user: str = Depends(get_current_user)):
    response.delete_cookie("session")
    response.delete_cookie("session_vars")
    repo_session: DbSessionRepository = DbSessionRepository(engine)
    await repo_session.delete_session("session_db")

    return {"ok": True}


@router.get("/signup")
async def signup(engine=Depends(create_db_engine)):
    signup_content = """
    <html lang='en'>
        <head>
          <meta charset="UTF-8">
          <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
          <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">

          <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"></script>
          <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>

        </head>
        <body>
          <div class="container">
            <h2>Sign Up Form</h2>
            <form>
                <div class="form-group">
                   <label for="firstname">Firstname:</label>
                   <input type='text' class="form-control" name='firstname' id='firstname'/><br/>
                </div>
                <div class="form-group">
                   <label for="lastname">Lastname:</label>
                   <input type='text' class="form-control" name='lastname' id='lastname'/><br/>
                </div>
                <div class="form-group">
                   <label for="username">Username:</label>
                   <input type='text' class="form-control" name='username' id='username'/><br/>
                </div>
                <div class="form-group">
                   <label for="password">Password:</label>
                   <input type='text' class="form-control" name='password' id='password'/><br/>
                </div>
                <div class="form-group">
                   <label for="role">Role:</label>
                   <input type='text' class="form-control" name='role' id='role'/><br/>
                </div>
                <button type="submit" class="btn btn-primary">Sign Up</button>
            </form>
           </div>
        </body>
    </html>
    """

    return HTMLResponse(content=signup_content, status_code=200)


@router.get("/login/html/list")
async def list_login_html(req: Request, engine=Depends(create_db_engine), user: str = Depends(get_current_user)):
    repo: LoginRepository = LoginRepository(engine)
    result = await repo.get_all_login()
    return templates.TemplateResponse("users.html", {"request": req, "data": result})


@router.get("/login/enc/details")
async def send_enc_login(engine=Depends(create_db_engine), user: str = Depends(get_current_user)):
    repo: LoginRepository = LoginRepository(engine)
    result = await repo.get_all_login();

    result_json = json.dumps(jsonable_encoder(result))
    fernet = Fernet(key)
    enc_data = fernet.encrypt(bytes(result_json, encoding='utf8'))

    return {"enc_data": enc_data, "key": key}


# app = FastAPI()
app = FastAPI(
        middleware=[
           Middleware(SessionMiddleware, secret_key='7UzGQS7woBazLUtVQJG39ywOP7J7lkPkB0UmDhMgBR8=',
                      session_cookie="session_vars"),
           Middleware(SessionDbMiddleware, sess_key='7UzGQS7woBazLUtVQJG39ywOP7J7lkPkB0UmDhMgBR8=', sess_name='session_db', expiry='2029-07-31')
            ],
            title="Related Blog Articles",
            description="This API was built with FastAPI and exists to find related blog articles given the ID of blog article.",
            version="1.0.0",
            servers=[
                {
                    "url": "http://localhost:8000",
                    "description": "Development Server"
                },
                {
                    "url": "https://localhost:8002",
                    "description": "Testing Server",
                }
            ])

app.add_middleware(CORSMiddleware,
                allow_origins=[
                    "https://localhost",
                    "http://localhost",
                    "https://localhost:8080",
                    "http://localhost:8080"
                ],
                allow_credentials=True,
                allow_methods=["POST", "GET", "DELETE", "PATCH", "PUT"],
                allow_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials", "Access-Control-Allow-Headers",
                               "Access-Control-Max-Age"],
                max_age=3600)


@router.get("/logina")
async def test_login(engine=Depends(create_db_engine), user: str = Depends(get_current_user)):
    return {"hello": "Good"}


@app.get("/")
async def test():
    return {"message": "Good"}
app.include_router(router, prefix='/sess')
app.mount("/static", StaticFiles(directory="static", html=True), name="static") # python working dir is current file dir


@app.on_event("startup")
async def initialize():
    create_db_connection()


@app.on_event("shutdown")
async def destroy():
    close_db_connection()


if __name__ == "__main__":
    uvicorn.run(app)