from pydantic import BaseModel
from typing import Optional, List, Dict, Any # Added List, Dict, Any
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    model_config = {'from_attributes': True}

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Project Schemas
class ProjectBase(BaseModel):
    project_name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    user_id: int
    last_modified: datetime
    # devices: List['Device'] = [] # Forward reference for relationships if needed directly in Project schema
    # links: List['Link'] = []   # Forward reference
    model_config = {'from_attributes': True}

# Device Schemas
class DeviceBase(BaseModel):
    device_type: str
    name: str
    properties: Dict[str, Any] # Stores x, y, bandwidth, ports etc.

class DeviceCreate(DeviceBase):
    client_id: Optional[str] = None # Temporary client-side ID

class Device(DeviceBase):
    id: int
    project_id: int
    model_config = {'from_attributes': True}

# Link Schemas
class LinkBase(BaseModel):
    # These will use client_ids when creating, but resolve to DB IDs for storage/retrieval
    source_port: Optional[str] = None
    target_port: Optional[str] = None

class LinkCreate(LinkBase):
    source_device_client_id: str # Refers to DeviceCreate.client_id
    target_device_client_id: str # Refers to DeviceCreate.client_id

class Link(LinkBase):
    id: int
    project_id: int
    source_device_id: int # Actual DB foreign key
    target_device_id: int # Actual DB foreign key
    model_config = {'from_attributes': True}

# Topology Schemas
class TopologyData(BaseModel): # For saving/loading an entire topology from client
    devices: List[DeviceCreate]
    links: List[LinkCreate]

class TopologyResponse(BaseModel): # For retrieving an entire topology to client
    devices: List[Device]
    links: List[Link]

# If using Pydantic v1, you might need this for forward references in Project schema
# Project.update_forward_refs()
