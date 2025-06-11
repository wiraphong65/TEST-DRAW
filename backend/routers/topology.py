from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List # For response models if needed, though Project and TopologyResponse are single objects

from .. import database, schemas, models, crud
from ..security import get_current_user
from .auth import get_db # Assuming get_db can be imported from auth router

router = APIRouter(
    prefix="/projects/{project_id}/topology",
    tags=["topology"]
)

@router.put("/", response_model=schemas.Project) # Returns the whole project, including updated topology
def update_topology_for_project(
    project_id: int,
    topology_data: schemas.TopologyData,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    updated_project = crud.update_project_topology(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
        topology_data=topology_data
    )
    if updated_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or not owned by user"
        )
    return updated_project

@router.get("/", response_model=schemas.TopologyResponse)
def get_topology_for_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    topology = crud.get_project_topology(
        db=db,
        project_id=project_id,
        user_id=current_user.id
    )
    if topology is None:
        # This implies the project itself wasn't found or not owned.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or not owned by user, or topology data is unavailable"
        )
    return topology
