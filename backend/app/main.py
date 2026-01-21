from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# ------------------ CORS (Frontend connection) ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ Upload directory ------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Make uploads accessible in browser
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# ------------------ AUTH (Simple demo) ------------------
users = {}

@app.post("/register")
def register(data: dict):
    email = data.get("email")
    password = data.get("password")

    if email in users:
        return {"error": "User already exists"}

    users[email] = password
    return {"message": "Registered successfully"}

@app.post("/login")
def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    if users.get(email) == password:
        return {"message": "Login success"}

    return {"error": "Invalid credentials"}

# ------------------ FILE UPLOAD ------------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}

# ------------------ LIST FILES ------------------
@app.get("/files")
def list_files():
    return os.listdir(UPLOAD_DIR)

# ------------------ DELETE FILE ------------------
@app.delete("/delete/{filename}")
def delete_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": "Deleted"}
    return {"error": "File not found"}
