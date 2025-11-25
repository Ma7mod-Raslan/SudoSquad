import string
import random
import time
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
import models, database

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

# -----------------------------
# Prometheus Metrics
# -----------------------------
URLS_SHORTENED = Counter("urls_shortened_total", "Total number of shortened URLs")
REDIRECTS = Counter("redirects_total", "Total successful redirects")
LOOKUP_404 = Counter("lookups_404_total", "Total number of 404 URL lookups")

REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"]
)


# -----------------------------
# Startup: DB + Boost Metrics
# -----------------------------
@app.on_event("startup")
def on_startup():
    max_retries = 10
    delay_seconds = 2

    # انتظار قاعدة البيانات
    for attempt in range(1, max_retries + 1):
        try:
            models.Base.metadata.create_all(bind=database.engine)
            print("✅ Database connected, tables created.")

            # ---- Boost the COUNTER based on existing DB records ----
            db = next(database.get_db())
            existing_urls = db.query(models.URL).count()

            if existing_urls > 0:
                URLS_SHORTENED.inc(existing_urls)
                print(f"🔄 Initialized Prometheus counter with {existing_urls} existing URLs.")

            break

        except OperationalError as e:
            print(f"❌ DB not ready (attempt {attempt}/{max_retries}): {e}")
            if attempt == max_retries:
                raise
            time.sleep(delay_seconds)


# -----------------------------
# Metrics Endpoint
# -----------------------------
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# -----------------------------
# Middleware for latency
# -----------------------------
class PromMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        elapsed = time.time() - start
        endpoint = request.url.path

        try:
            REQUEST_LATENCY.labels(endpoint=endpoint).observe(elapsed)
        except Exception:
            pass

        return response

app.add_middleware(PromMiddleware)


# -----------------------------
# Helpers
# -----------------------------
def generate_short_code(length: int = 6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


# -----------------------------
# ROUTES
# -----------------------------
@app.get("/stats")
def get_stats(db: Session = Depends(database.get_db)):
    total_urls = db.query(models.URL).count()
    return {"total_urls": total_urls}


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
            LOOKUP_404.inc()
            raise HTTPException(status_code=404, detail="URL not found")

        REDIRECTS.inc()
        return RedirectResponse(url=db_url.long_url)

    finally:
        elapsed = time.perf_counter() - start_time
        REQUEST_LATENCY.labels(endpoint="redirect").observe(elapsed)

app.mount("/static", StaticFiles(directory="/app/static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("/app/static/index.html")
