from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas
from .security import get_password_hash

# User CRUD operations
def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Project CRUD operations
def create_user_project(db: Session, project: schemas.ProjectCreate, user_id: int) -> models.Project:
    db_project = models.Project(**project.model_dump(), user_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_projects_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Project]:
    return db.query(models.Project).filter(models.Project.user_id == user_id).offset(skip).limit(limit).all()

def get_project(db: Session, project_id: int, user_id: int) -> Optional[models.Project]:
    return db.query(models.Project).filter(models.Project.id == project_id, models.Project.user_id == user_id).first()

def update_project(db: Session, project_id: int, project_update: schemas.ProjectCreate, user_id: int) -> Optional[models.Project]:
    db_project = get_project(db=db, project_id=project_id, user_id=user_id)
    if db_project:
        update_data = project_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_project, key, value)
        db.commit()
        db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int, user_id: int) -> Optional[models.Project]:
    db_project = get_project(db=db, project_id=project_id, user_id=user_id)
    if db_project:
        db.delete(db_project)
        db.commit()
    # Return the project object that was deleted, or None if not found
    # Note: After deletion, accessing attributes of db_project might be problematic
    # if the session is expired or the object is no longer tracked.
    # For some use cases, it might be better to return a simple confirmation or the ID.
    return db_project

# Topology CRUD operations
def update_project_topology(db: Session, project_id: int, user_id: int, topology_data: schemas.TopologyData) -> Optional[models.Project]:
    db_project = get_project(db=db, project_id=project_id, user_id=user_id)
    if not db_project:
        return None # Or raise HTTPException

    # Clear existing links and devices for this project
    # synchronize_session=False is recommended for bulk deletes before a commit.
    db.query(models.Link).filter(models.Link.project_id == project_id).delete(synchronize_session=False)
    db.query(models.Device).filter(models.Device.project_id == project_id).delete(synchronize_session=False)
    # It's often better to commit deletions separately or ensure they are flushed before adding new items
    # if there are constraints or potential ID conflicts, but here we are recreating.
    # db.commit() # Optional: commit deletions first

    client_to_db_id_map = {}
    new_devices_for_db = []

    # Create new devices
    for device_data in topology_data.devices:
        db_device = models.Device(
            project_id=project_id,
            name=device_data.name,
            device_type=device_data.device_type,
            properties=device_data.properties
        )
        db.add(db_device)
        new_devices_for_db.append(db_device) # Keep track for client_id mapping

    # Flush to get IDs for newly added devices before creating links
    # This is crucial for links to reference correct device IDs.
    db.flush()

    for i, device_data in enumerate(topology_data.devices):
        if device_data.client_id:
            # new_devices_for_db[i] should correspond to device_data due to order of processing
            client_to_db_id_map[device_data.client_id] = new_devices_for_db[i].id

    # Create new links
    for link_data in topology_data.links:
        source_db_id = client_to_db_id_map.get(link_data.source_device_client_id)
        target_db_id = client_to_db_id_map.get(link_data.target_device_client_id)

        if source_db_id is not None and target_db_id is not None:
            db_link = models.Link(
                project_id=project_id,
                source_device_id=source_db_id,
                target_device_id=target_db_id,
                source_port=link_data.source_port,
                target_port=link_data.target_port
            )
            db.add(db_link)
        else:
            # Handle error: client_id not found. Log or raise.
            # For now, we'll skip creating this link.
            print(f"Warning: Could not resolve client_ids for link: {link_data.source_device_client_id} -> {link_data.target_device_client_id}")


    db.commit()
    db.refresh(db_project) # Refresh to load the new devices and links relationships
    return db_project

def get_project_topology(db: Session, project_id: int, user_id: int) -> Optional[schemas.TopologyResponse]:
    db_project = get_project(db=db, project_id=project_id, user_id=user_id)
    if not db_project:
        return None

    # Devices and links are loaded via relationships defined in models.Project
    # Convert ORM models to Pydantic schemas for the response
    devices_schema = [schemas.Device.model_validate(device) for device in db_project.devices]
    links_schema = [schemas.Link.model_validate(link) for link in db_project.links]

    return schemas.TopologyResponse(devices=devices_schema, links=links_schema)
