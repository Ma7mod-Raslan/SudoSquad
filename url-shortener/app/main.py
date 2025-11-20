import string
import random
import time 
from fastapi import FastAPI, Depends, HTTPException, Response 
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError  
import models, database

app = FastAPI()

@app.on_event("startup")
def on_startup():
    max_retries = 10
    delay_seconds = 2

    for attempt in range(1, max_retries + 1):
        try:
            models.Base.metadata.create_all(bind=database.engine)
            print("✅ Database connected, tables created (or already exist).")
            break
        except OperationalError as e:
            print(f"❌ DB not ready yet (attempt {attempt}/{max_retries}): {e}")
            if attempt == max_retries:
                raise
            time.sleep(delay_seconds)

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST


app.mount("/static", StaticFiles(directory="static"), name="static")


URLS_SHORTENED = Counter(
    "url_shortener_urls_shortened_total",
    "Number of URLs successfully shortened",
)

REDIRECTS_SUCCESS = Counter(
    "url_shortener_redirects_total",
    "Number of successful redirects",
)

LOOKUPS_FAILED = Counter(
    "url_shortener_not_found_total",
    "Number of failed lookups (404 errors)",
)

REQUEST_LATENCY = Histogram(
    "url_shortener_request_latency_seconds",
    "Request latency for URL creation and redirects",
    ["endpoint"],  
)

def generate_short_code(length: int = 6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

@app.get("/stats")
def get_stats(db: Session = Depends(database.get_db)):
    total_urls = db.query(models.URL).count()
    return {"total_urls": total_urls}

@app.get("/metrics")
def metrics():
    """Expose Prometheus metrics."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/shorten")
def create_short_url(long_url: str, db: Session = Depends(database.get_db)):
    start_time = time.perf_counter()
    try:
        if not long_url.startswith("http"):
            raise HTTPException(status_code=400, detail="Invalid URL format")

        short_code = generate_short_code()
        db_url = models.URL(short_code=short_code, long_url=long_url)
        db.add(db_url)
        db.commit()
        db.refresh(db_url)

        URLS_SHORTENED.inc()
        return {"short_code": short_code}
    finally:
        elapsed = time.perf_counter() - start_time
        REQUEST_LATENCY.labels(endpoint="shorten").observe(elapsed)

@app.get("/{short_code}")
def redirect_to_long_url(short_code: str, db: Session = Depends(database.get_db)):
    start_time = time.perf_counter()
    try:
        db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
        if db_url is None:
            LOOKUPS_FAILED.inc()
            raise HTTPException(status_code=404, detail="URL not found")

        REDIRECTS_SUCCESS.inc()
        return RedirectResponse(url=db_url.long_url)
    finally:
        elapsed = time.perf_counter() - start_time
        REQUEST_LATENCY.labels(endpoint="redirect").observe(elapsed)

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")
