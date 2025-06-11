from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

    projects = relationship("Project", back_populates="owner")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_name = Column(String, index=True)
    description = Column(String, nullable=True)
    last_modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="projects")
    devices = relationship("Device", back_populates="project", cascade="all, delete-orphan")
    links = relationship("Link", back_populates="project", cascade="all, delete-orphan")

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    device_type = Column(String)  # E.g., "Router", "Switch", "PC", "Server", "Firewall"
    name = Column(String)
    properties = Column(JSON)  # Stores bandwidth, ports, throughput_per_port, estimated_load, x_position, y_position

    project = relationship("Project", back_populates="devices")
    # Relationships for links originating from this device
    source_links = relationship("Link", foreign_keys="Link.source_device_id", back_populates="source_device", cascade="all, delete-orphan")
    # Relationships for links terminating at this device
    target_links = relationship("Link", foreign_keys="Link.target_device_id", back_populates="target_device", cascade="all, delete-orphan")

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    source_device_id = Column(Integer, ForeignKey("devices.id"))
    target_device_id = Column(Integer, ForeignKey("devices.id"))
    source_port = Column(String, nullable=True)  # Name/ID of the port on the source device
    target_port = Column(String, nullable=True)  # Name/ID of the port on the target device

    project = relationship("Project", back_populates="links")
    source_device = relationship("Device", foreign_keys=[source_device_id], back_populates="source_links")
    target_device = relationship("Device", foreign_keys=[target_device_id], back_populates="target_links")
