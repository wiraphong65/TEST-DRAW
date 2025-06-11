from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, schemas, models, crud # Adjusted for direct imports from package root
from ..security import get_current_user
from .auth import get_db # Assuming get_db can be imported from auth router

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

@router.post("/", response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_user_project(db=db, project=project, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Project])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    projects = crud.get_projects_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return projects

@router.get("/{project_id}", response_model=schemas.Project)
def read_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_project = crud.get_project(db=db, project_id=project_id, user_id=current_user.id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return db_project

@router.put("/{project_id}", response_model=schemas.Project)
def update_existing_project(
    project_id: int,
    project_update: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    updated_project = crud.update_project(db=db, project_id=project_id, project_update=project_update, user_id=current_user.id)
    if updated_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found or not owned by user")
    return updated_project

@router.delete("/{project_id}", response_model=schemas.Project) # Or return a status code like 204 No Content
def delete_existing_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    deleted_project = crud.delete_project(db=db, project_id=project_id, user_id=current_user.id)
    if deleted_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found or not owned by user")
    return deleted_project
