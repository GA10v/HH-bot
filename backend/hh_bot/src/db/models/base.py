from db.pg_db import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, TIMESTAMP, inspect
import uuid
import datetime


class BaseModel(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    create_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    modified = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    def _asdict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
