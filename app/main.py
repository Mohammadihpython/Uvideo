import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette_exporter import PrometheusMiddleware,handle_metrics


from .routers import auth,video_service

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)
app.include_router(auth.router)
app.include_router(video_service.router)

@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}


if __name__ == '__main__':
    uvicorn.run("main:app",
                )
