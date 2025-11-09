import string
import random
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Mount the 'static' directory to serve files from '/static' path
app.mount("/static", StaticFiles(directory="static"), name="static")


def generate_short_code(length: int = 6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

# NEW: Endpoint to get application statistics
@app.get("/stats")
def get_stats(db: Session = Depends(database.get_db)):
    total_urls = db.query(models.URL).count()
    return {"total_urls": total_urls}

# API Endpoint to create a short URL
@app.post("/shorten")
def create_short_url(long_url: str, db: Session = Depends(database.get_db)):
    # Basic validation
    if not long_url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL format")

    short_code = generate_short_code()
    db_url = models.URL(short_code=short_code, long_url=long_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return {"short_code": short_code}

# API Endpoint to handle the redirect
@app.get("/{short_code}")
def redirect_to_long_url(short_code: str, db: Session = Depends(database.get_db)):
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=db_url.long_url)

# Endpoint to serve the main HTML page
@app.get("/")
async def read_index():
    return FileResponse('static/index.html')