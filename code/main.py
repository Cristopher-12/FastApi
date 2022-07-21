from urllib import response
from fastapi import FastAPI, HTTPException, status, Depends, Security, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
import hashlib
import pyrebase

app = FastAPI()

firebaseConfig = {
    "apiKey": "AIzaSyDCRXcqOhIIrB1ouzD5CFebw9yFqvPFwBM",
    "authDomain": "fastapi-9c26c.firebaseapp.com",
    "databaseURL": "https://fastapi-9c26c-default-rtdb.firebaseio.com",
    "projectId": "fastapi-9c26c",
    "storageBucket": "fastapi-9c26c.appspot.com",
    "messagingSenderId": "616263160176",
    "appId": "1:616263160176:web:2e8f211bb49864acb9bfb5"
  };

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
db = firebase.database()

email = "cristopher@email.com"

password_b = hashlib.md5("".encode())
password = password_b.hexdigest()

securityBasic = HTTPBasic()
securityBearer = HTTPBearer()


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url='/docs')

@app.get(
    "/user/validate/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get a token for a user",
    description="Get a token for a user",
    tags=["auth"],
  )
async def get_token(credentials: HTTPBasicCredentials = Depends(securityBasic)):
    try:
      user = credentials.username
      password = credentials.password
      user = auth.sign_in_with_email_and_password(email, password)
      response = {
        "token": user['idToken'],
      }
      return response
    except Exception as e:
      print(f"Error: {e}")
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e)

@app.get(
  "/user/",
  status_code=status.HTTP_202_ACCEPTED,
  summary="Get a token for a user",
  description="Get a token for a user",
  tags=["auth"],
)
async def get_token_bearer(credentials: HTTPAuthorizationCredentials =  Depends(securityBearer)):
    try:
      user = auth.get_account_info(credentials.credentials)
      uid = user['users'][0]['localId']
      users_data = db.child("users").child(uid).get().val()
      response = {
        "user": users_data,
      }
      return response
    except Exception as e:
      print(f"Error: {e}")
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e)