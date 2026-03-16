from typing import Any, Optional
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from enum import Enum as SQLAlchemyEnum

Base = declarative_base()

class StepType(SQLAlchemyEnum):
    SIMPLE = 'simple'
    COMPLEX = 'complex'
    STREAMING = 'streaming'

class FlowTemplate(Base):
    __tablename__ = 'flow_template'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    steps = relationship("FlowStep", back_populates="template")

class FlowStep(Base):
    __tablename__ = 'flow_step'
    id = Column(Integer, primary_key=True)
    step_type = Column(Enum(StepType), nullable=False)
    step_data = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    template_id = Column(Integer, ForeignKey('flow_template.id'), nullable=False)
    template = relationship("FlowTemplate", back_populates="steps")

# Database setup
DATABASE_URL = get_config()['database_url']
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
Session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
db.session = Session()