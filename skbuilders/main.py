from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routers import projects, quotes, auth

# Create DB tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SK Builders API",
    description="Backend API for SK Builders Construction website",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded project images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Routers
app.include_router(auth.router,     prefix="/api/auth",     tags=["Auth"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(quotes.router,   prefix="/api/quotes",   tags=["Quotes"])


@app.get("/")
def root():
    return {"message": "SK Builders API is running!"}
