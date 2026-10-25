import os
from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine, get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    Handles startup and shutdown events cleanly without blocking module import.
    In development, tables are auto-created if AUTO_CREATE_TABLES=true.
    In production / K8s, database migrations or Helm pre-sync jobs manage DDL.
    """
    if os.getenv("AUTO_CREATE_TABLES", "true").lower() in ("true", "1", "yes"):
        try:
            models.Base.metadata.create_all(bind=engine)
        except Exception as exc:
            print(f"[WARN] Failed to auto-create tables on startup: {exc}")
    yield

app = FastAPI(
    title="LaunchWeave API",
    description="Cloud-native Task Management REST API built with FastAPI and PostgreSQL.",
    version="0.1.0",
    lifespan=lifespan,
)

@app.get("/healthz", tags=["Probes"])
async def healthz():
    """Liveness probe: returns 200 OK if the process is running."""
    return {"status": "healthy"}

@app.get("/readyz", tags=["Probes"])
def readyz(db: Session = Depends(get_db)):
    """
    Readiness probe: verifies database connectivity.
    If the database is unreachable, returns 503 so Kubernetes / load balancers
    avoid routing traffic to this replica until it is truly ready.
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database unreachable: {exc}",
        )

@app.get("/tasks", response_model=List[schemas.TaskResponse], tags=["Tasks"])
def read_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)

@app.post("/tasks", response_model=schemas.TaskResponse, status_code=201, tags=["Tasks"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db=db, task_id=task_id, task_update=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = crud.delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
