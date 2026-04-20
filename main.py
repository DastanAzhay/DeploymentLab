from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI()
security = HTTPBearer()

# Configuration
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Sample user database
users = [
    {"id": 1, "username": "admin", "password": "adminpass", "role": "admin"},
]

# Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

# JWT token creation
def create_access_token(username: str, expires_delta: Optional[timedelta] = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    expire = datetime.utcnow() + expires_delta
    payload = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# JWT token verification
def verify_token(credentials: HTTPAuthCredentials = Depends(security)) -> str:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Helper function to find user
def get_user(username: str):
    for user in users:
        if user["username"] == username:
            return user
    return None

# Endpoints
@app.post("/register", response_model=TokenResponse)
def register(user_data: UserCreate):
    if get_user(user_data.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = {
        "id": len(users) + 1,
        "username": user_data.username,
        "password": user_data.password,
        "role": user_data.role
    }
    users.append(new_user)
    access_token = create_access_token(user_data.username)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login", response_model=TokenResponse)
def login(username: str, password: str):
    user = get_user(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(username)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=UserResponse)
def get_current_user(username: str = Depends(verify_token)):
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(id=user["id"], username=user["username"], role=user["role"])

