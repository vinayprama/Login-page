from fastapi import FastAPI, HTTPException, Depends, Header
from backend.database import get_db
from backend.schemas import UserRegister, UserLogin, ResetPassword
from backend.auth import create_jwt, decode_jwt
import bcrypt
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os




app = FastAPI()

frontend_path = os.path.join(os.getcwd(), "frontend")

# ✅ Serve Static Files (CSS, JS)
app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")

# ✅ Serve HTML Files
@app.get("/")
def serve_home():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/register")
def serve_register():
    return FileResponse(os.path.join(frontend_path, "register.html"))

@app.get("/reset")
def serve_reset():
    return FileResponse(os.path.join(frontend_path, "reset.html"))

@app.get("/welcome")
def serve_welcome():
    return FileResponse(os.path.join(frontend_path, "welcome.html"))




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],
)



@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html")

@app.post("/register/")
def register(user: UserRegister):
    db = get_db()
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    try:
        db.execute("INSERT INTO users (username, password, security_question, security_answer) VALUES (?, ?, ?, ?)",
                   (user.username, hashed_pw, user.security_question, user.security_answer))
        db.commit()
        return {"message": "User registered successfully"}
    except:
        raise HTTPException(status_code=400, detail="Username already exists")

@app.post("/login/")
def login(user: UserLogin):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT password FROM users WHERE username = ?", (user.username,))
    record = cur.fetchone()

    if record and bcrypt.checkpw(user.password.encode(), record[0].encode()):
        token = create_jwt(user.username)
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/reset-password/")
def reset_password(user: ResetPassword):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT security_answer FROM users WHERE username = ?", (user.username,))
    record = cur.fetchone()

    if record and record[0] == user.security_answer:
        hashed_pw = bcrypt.hashpw(user.new_password.encode(), bcrypt.gensalt()).decode()
        db.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_pw, user.username))
        db.commit()
        return {"message": "Password reset successfully"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect security answer")

@app.get("/welcome/")
def welcome(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    token = authorization.split(" ")[1]
    username = decode_jwt(token)

    if username:
        return {"message": f"Welcome {username}!"}
    else:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
