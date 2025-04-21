from fastapi import FastAPI
from app.routes import stories, stats, auth

app = FastAPI(
    title="Hacker News Pipeline API",
    description="This API provides access to top Hacker News stories, user authentication, and statistics endpoints.",
    version="1.0.0"
)

# Include the authentication router
app.include_router(auth.router, tags=["Authentication"])

# Include the stories router
app.include_router(stories.router, tags=["Stories"])

# Include the statistics router
app.include_router(stats.router, tags=["Statistics"])
